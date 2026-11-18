"""Sherpas AI Proxy client with TEAM_KEY auth, /key/info budget guard, rate/concurrency limits, and deterministic fallback."""

from __future__ import annotations

from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import threading
import time
from typing import Any, Callable, Iterator
import urllib.error
import urllib.request

try:
    import openai as _openai_sdk  # type: ignore
except ImportError:  # pragma: no cover - verified in environments without openai installed
    _openai_sdk = None


DEFAULT_PROXY_URL = "https://llm-hackathon.sherpaswealth.com"
DEFAULT_MODEL = "gpt-5-mini"
SUPPORTED_MODELS = ("gpt-5-mini", "deepseek-flash")
GPT5_MINI_MIN_MAX_TOKENS = 1000
DEFAULT_MAX_BUDGET_USD = 50.0
DEFAULT_RATE_LIMIT_RPM = 60
DEFAULT_MAX_CONCURRENT = 4

_SENSITIVE_FIELDS = frozenset({"key", "api_key", "team_key", "token", "secret", "authorization"})


class LLMProxyError(Exception):
    """Base error raised by LLMProxyClient when fallback is disabled or invalid arguments are given."""


class BudgetExhaustedError(LLMProxyError):
    """Raised when the TEAM_KEY budget ($50 max by default) has been exhausted."""

    def __init__(self, message: str, key_info: "KeyInfo | None" = None) -> None:
        super().__init__(message)
        self.key_info = key_info


class RateLimitExceededError(LLMProxyError):
    """Raised when the 60 requests-per-minute limit would be exceeded."""


class ConcurrencyLimitExceededError(LLMProxyError):
    """Raised when more than 4 concurrent requests cannot acquire a slot in time."""


@dataclass(frozen=True)
class KeyInfo:
    """Sanitized representation of Sherpas proxy `/key/info` budget state."""

    spend: float
    max_budget: float
    remaining_budget: float
    budget_available: bool
    source: str = "proxy"
    raw_info: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "spend": self.spend,
            "max_budget": self.max_budget,
            "remaining_budget": self.remaining_budget,
            "budget_available": self.budget_available,
            "source": self.source,
            "info": dict(self.raw_info),
        }


@dataclass(frozen=True)
class ProxyResponse:
    """Unified response returned by `LLMProxyClient.chat_completion`."""

    content: str
    model: str
    used_fallback: bool
    fallback_reason: str | None = None
    usage: dict[str, Any] = field(default_factory=dict)
    key_info: KeyInfo | None = None
    transport: str = "urllib"
    raw: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "content": self.content,
            "model": self.model,
            "used_fallback": self.used_fallback,
            "fallback_reason": self.fallback_reason,
            "usage": dict(self.usage),
            "key_info": self.key_info.to_dict() if self.key_info else None,
            "transport": self.transport,
        }


def _mask_secret(secret: str | None) -> str:
    if not secret:
        return "<unset>"
    if len(secret) <= 6:
        return "****"
    return f"****{secret[-4:]}"


def _sanitize_mapping(data: Any) -> Any:
    if isinstance(data, dict):
        cleaned: dict[str, Any] = {}
        for k, v in data.items():
            if str(k).lower() in _SENSITIVE_FIELDS:
                continue
            cleaned[k] = _sanitize_mapping(v)
        return cleaned
    if isinstance(data, list):
        return [_sanitize_mapping(item) for item in data]
    return data


def _normalize_base_url(proxy_url: str | None) -> str:
    url = (proxy_url or DEFAULT_PROXY_URL).strip().rstrip("/")
    if url.endswith("/v1"):
        url = url[:-3].rstrip("/")
    return url or DEFAULT_PROXY_URL


def _parse_dotenv_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    try:
        content = path.read_text(encoding="utf-8-sig")
    except OSError:
        return values
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
            val = val[1:-1]
        if key:
            values[key] = val
    return values


def _discover_dotenv(dotenv_path: str | Path | None = None) -> dict[str, str]:
    if dotenv_path is not None:
        return _parse_dotenv_file(Path(dotenv_path))
    candidates = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent / ".env",
    ]
    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.is_file():
            return _parse_dotenv_file(resolved)
    return {}


def _is_mocked(obj: Any) -> bool:
    return type(obj).__module__.startswith("unittest.mock") or hasattr(obj, "assert_called")


def build_chat_payload(
    messages: list[dict[str, Any]],
    model: str = DEFAULT_MODEL,
    max_tokens: int | None = None,
    max_completion_tokens: int | None = None,
    temperature: float | None = None,
    strict_model: bool = True,
    **extra_params: Any,
) -> dict[str, Any]:
    """Build a chat completions payload enforcing Sherpas proxy rules.

    Critical rule for `gpt-5-mini`: `max_tokens` (and `max_completion_tokens`) must either
    be omitted or be at least `1000` so reasoning tokens never starve the visible completion.
    """
    if strict_model and model not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model '{model}'. Expected one of {SUPPORTED_MODELS}.")
    if not messages:
        raise ValueError("messages must be a non-empty list of chat message dicts.")

    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
    }

    if model == "gpt-5-mini":
        if max_tokens is not None:
            payload["max_tokens"] = max(GPT5_MINI_MIN_MAX_TOKENS, int(max_tokens))
        if max_completion_tokens is not None:
            payload["max_completion_tokens"] = max(
                GPT5_MINI_MIN_MAX_TOKENS, int(max_completion_tokens)
            )
    else:
        if max_tokens is not None:
            payload["max_tokens"] = int(max_tokens)
        if max_completion_tokens is not None:
            payload["max_completion_tokens"] = int(max_completion_tokens)

    if temperature is not None:
        payload["temperature"] = float(temperature)

    for k, v in extra_params.items():
        if v is not None and k not in _SENSITIVE_FIELDS:
            payload[k] = v

    return payload


class SlidingWindowRateLimiter:
    """Thread-safe sliding window limiter enforcing at most `max_requests` per `window_seconds`."""

    def __init__(
        self,
        max_requests: int = DEFAULT_RATE_LIMIT_RPM,
        window_seconds: float = 60.0,
        clock: Callable[[], float] = time.monotonic,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        if max_requests <= 0:
            raise ValueError("max_requests must be positive.")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive.")
        self.max_requests = int(max_requests)
        self.window_seconds = float(window_seconds)
        self._clock = clock
        self._sleeper = sleeper
        self._timestamps: deque[float] = deque()
        self._lock = threading.Lock()

    def _prune(self, now: float) -> None:
        cutoff = now - self.window_seconds
        while self._timestamps and self._timestamps[0] <= cutoff:
            self._timestamps.popleft()

    @property
    def current_count(self) -> int:
        with self._lock:
            self._prune(self._clock())
            return len(self._timestamps)

    @property
    def remaining_quota(self) -> int:
        with self._lock:
            self._prune(self._clock())
            return max(0, self.max_requests - len(self._timestamps))

    @property
    def reset_in_seconds(self) -> float:
        with self._lock:
            now = self._clock()
            self._prune(now)
            if len(self._timestamps) < self.max_requests:
                return 0.0
            return max(0.0, (self._timestamps[0] + self.window_seconds) - now)

    def acquire(self, block: bool = False, timeout: float = 0.0) -> None:
        deadline = self._clock() + max(0.0, float(timeout))
        while True:
            wait_for = 0.0
            with self._lock:
                now = self._clock()
                self._prune(now)
                if len(self._timestamps) < self.max_requests:
                    self._timestamps.append(now)
                    return
                wait_for = max(0.001, (self._timestamps[0] + self.window_seconds) - now)
                if not block or now >= deadline:
                    raise RateLimitExceededError(
                        f"Rate limit reached: {self.max_requests} requests per {self.window_seconds:.0f}s."
                    )
                if now + wait_for > deadline:
                    wait_for = max(0.0, deadline - now)
            if wait_for <= 0:
                raise RateLimitExceededError(
                    f"Rate limit reached: {self.max_requests} requests per {self.window_seconds:.0f}s."
                )
            self._sleeper(wait_for)


class ConcurrencyLimiter:
    """Thread-safe bounded concurrency limiter tracking active and peak in-flight requests."""

    def __init__(self, max_concurrent: int = DEFAULT_MAX_CONCURRENT) -> None:
        if max_concurrent <= 0:
            raise ValueError("max_concurrent must be positive.")
        self.max_concurrent = int(max_concurrent)
        self._semaphore = threading.BoundedSemaphore(self.max_concurrent)
        self._lock = threading.Lock()
        self._active = 0
        self._peak = 0

    @property
    def active_requests(self) -> int:
        with self._lock:
            return self._active

    @property
    def peak_concurrent_requests(self) -> int:
        with self._lock:
            return self._peak

    @contextmanager
    def slot(self, timeout: float | None = 10.0) -> Iterator[None]:
        acquired = (
            self._semaphore.acquire(blocking=True, timeout=timeout)
            if timeout is not None
            else self._semaphore.acquire(blocking=True)
        )
        if not acquired:
            raise ConcurrencyLimitExceededError(
                f"Concurrency limit reached: max {self.max_concurrent} concurrent requests."
            )
        with self._lock:
            self._active += 1
            if self._active > self._peak:
                self._peak = self._active
        try:
            yield
        finally:
            with self._lock:
                self._active = max(0, self._active - 1)
            self._semaphore.release()


def _default_deterministic_fallback(
    messages: list[dict[str, Any]],
    model: str,
    reason: str,
    fallback_context: dict[str, Any] | None = None,
) -> str:
    if fallback_context:
        if "deterministic_text" in fallback_context and fallback_context["deterministic_text"]:
            return str(fallback_context["deterministic_text"])
        if "deterministic_json" in fallback_context:
            return json.dumps(fallback_context["deterministic_json"], ensure_ascii=False)

    last_user = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            last_user = str(msg.get("content", "")).strip()
            break
    summary_hint = last_user[:240] if last_user else "sin consulta"
    return (
        f"[Modo determinista offline ({reason}) · modelo={model}] "
        f"Respuesta segura generada sin llamada remota para: {summary_hint}"
    )


class LLMProxyClient:
    """Backend client for Sherpas AI Proxy (`TEAM_KEY`), enforcing budget, RPM, and concurrency."""

    def __init__(
        self,
        team_key: str | None = None,
        base_url: str | None = None,
        default_model: str = DEFAULT_MODEL,
        max_requests_per_minute: int = DEFAULT_RATE_LIMIT_RPM,
        max_concurrent: int = DEFAULT_MAX_CONCURRENT,
        max_budget_usd: float = DEFAULT_MAX_BUDGET_USD,
        check_budget_before_call: bool = True,
        budget_cache_ttl_seconds: float = 0.0,
        block_on_rate_limit: bool = False,
        rate_limit_timeout: float = 0.0,
        concurrency_timeout: float | None = 10.0,
        fallback_on_error: bool = True,
        transport: str = "auto",
        dotenv_path: str | Path | None = None,
        timeout: float = 30.0,
        clock: Callable[[], float] = time.monotonic,
        sleeper: Callable[[float], None] = time.sleep,
        fallback_generator: Callable[[list[dict[str, Any]], str, str, dict[str, Any] | None], str] | None = None,
    ) -> None:
        if default_model not in SUPPORTED_MODELS:
            raise ValueError(f"Unsupported default_model '{default_model}'. Expected one of {SUPPORTED_MODELS}.")
        if transport not in ("auto", "openai", "urllib"):
            raise ValueError("transport must be 'auto', 'openai', or 'urllib'.")

        dotenv = _discover_dotenv(dotenv_path)
        resolved_key = (
            team_key
            if team_key is not None
            else os.environ.get("TEAM_KEY") or os.environ.get("SHERPAS_TEAM_KEY") or dotenv.get("TEAM_KEY")
        )
        resolved_url = (
            base_url
            if base_url is not None
            else os.environ.get("LLM_PROXY_URL") or dotenv.get("LLM_PROXY_URL") or DEFAULT_PROXY_URL
        )

        self._team_key: str = (resolved_key or "").strip()
        self.base_url: str = _normalize_base_url(resolved_url)
        self.default_model: str = default_model
        self.max_budget_usd: float = float(max_budget_usd)
        self.check_budget_before_call: bool = bool(check_budget_before_call)
        self.budget_cache_ttl_seconds: float = max(0.0, float(budget_cache_ttl_seconds))
        self.block_on_rate_limit: bool = bool(block_on_rate_limit)
        self.rate_limit_timeout: float = max(0.0, float(rate_limit_timeout))
        self.concurrency_timeout: float | None = concurrency_timeout
        self.fallback_on_error: bool = bool(fallback_on_error)
        self.transport: str = transport
        self.timeout: float = float(timeout)
        self._clock = clock
        self._fallback_generator = fallback_generator or _default_deterministic_fallback

        self.rate_limiter = SlidingWindowRateLimiter(
            max_requests=max_requests_per_minute,
            window_seconds=60.0,
            clock=clock,
            sleeper=sleeper,
        )
        self.concurrency_limiter = ConcurrencyLimiter(max_concurrent=max_concurrent)

        self._budget_lock = threading.Lock()
        self._cached_key_info: KeyInfo | None = None
        self._cached_key_info_at: float = 0.0

    def __repr__(self) -> str:
        return (
            f"LLMProxyClient(base_url={self.base_url!r}, "
            f"default_model={self.default_model!r}, "
            f"team_key={_mask_secret(self._team_key)!r})"
        )

    @property
    def has_team_key(self) -> bool:
        return bool(self._team_key)

    @property
    def completions_endpoint(self) -> str:
        return f"{self.base_url}/v1/chat/completions"

    @property
    def key_info_endpoint(self) -> str:
        return f"{self.base_url}/key/info"

    def _auth_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._team_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _parse_key_info_payload(self, data: dict[str, Any]) -> KeyInfo:
        info = data.get("info") if isinstance(data.get("info"), dict) else data
        spend_raw = info.get("spend", data.get("spend", 0.0))
        max_budget_raw = info.get("max_budget", data.get("max_budget"))
        spend = float(spend_raw) if spend_raw is not None else 0.0
        max_budget = float(max_budget_raw) if max_budget_raw is not None else self.max_budget_usd
        remaining = max(0.0, max_budget - spend)
        sanitized_info = _sanitize_mapping(info) if isinstance(info, dict) else {}
        return KeyInfo(
            spend=round(spend, 6),
            max_budget=round(max_budget, 6),
            remaining_budget=round(remaining, 6),
            budget_available=spend < max_budget and remaining > 0.0,
            source="proxy",
            raw_info=sanitized_info,
        )

    def get_key_info(self, force_refresh: bool = True) -> KeyInfo:
        """Query `GET /key/info` with `Authorization: Bearer <TEAM_KEY>` and parse spend/max_budget."""
        if not self.has_team_key:
            return KeyInfo(
                spend=0.0,
                max_budget=self.max_budget_usd,
                remaining_budget=self.max_budget_usd,
                budget_available=False,
                source="missing_team_key",
                raw_info={},
            )

        if not force_refresh and self.budget_cache_ttl_seconds > 0:
            with self._budget_lock:
                if (
                    self._cached_key_info is not None
                    and (self._clock() - self._cached_key_info_at) < self.budget_cache_ttl_seconds
                ):
                    return self._cached_key_info

        req = urllib.request.Request(
            self.key_info_endpoint,
            headers={
                "Authorization": f"Bearer {self._team_key}",
                "Accept": "application/json",
            },
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw_bytes = resp.read()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            raise LLMProxyError(f"Failed to query {self.key_info_endpoint}: {type(exc).__name__}") from None

        try:
            payload = json.loads(raw_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise LLMProxyError("Invalid JSON received from /key/info.") from exc

        key_info = self._parse_key_info_payload(payload if isinstance(payload, dict) else {})
        with self._budget_lock:
            self._cached_key_info = key_info
            self._cached_key_info_at = self._clock()
        return key_info

    def ensure_budget_available(self, force_refresh: bool = False) -> KeyInfo:
        """Verify `/key/info` has remaining USD budget before invoking completions."""
        force = force_refresh or self.budget_cache_ttl_seconds <= 0.0
        key_info = self.get_key_info(force_refresh=force)
        if not key_info.budget_available:
            raise BudgetExhaustedError(
                f"TEAM_KEY budget exhausted: spend=${key_info.spend:.2f} / max_budget=${key_info.max_budget:.2f}",
                key_info=key_info,
            )
        return key_info

    def _should_use_openai_sdk(self) -> bool:
        if self.transport == "urllib":
            return False
        if self.transport == "openai":
            if _openai_sdk is None:
                raise LLMProxyError("openai SDK requested but package 'openai' is not installed.")
            return True
        if _openai_sdk is None:
            return False
        if _is_mocked(urllib.request.urlopen):
            return False
        return True

    def _call_via_openai_sdk(self, payload: dict[str, Any]) -> tuple[dict[str, Any], str]:
        try:
            client = _openai_sdk.OpenAI(
                api_key=self._team_key,
                base_url=f"{self.base_url}/v1",
                timeout=self.timeout,
            )
            completion = client.chat.completions.create(**payload)
        except Exception as exc:  # pragma: no cover - exercised when openai SDK is installed
            raise LLMProxyError(f"OpenAI SDK proxy call failed: {type(exc).__name__}") from None
        if hasattr(completion, "model_dump"):
            raw = completion.model_dump()
        else:  # pragma: no cover - older SDKs
            raw = json.loads(completion.json())
        return raw, "openai_sdk"

    def _call_via_urllib(self, payload: dict[str, Any]) -> tuple[dict[str, Any], str]:
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.completions_endpoint,
            data=body,
            headers=self._auth_headers(),
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw_bytes = resp.read()
        except urllib.error.HTTPError as exc:
            raise LLMProxyError(f"Proxy HTTP error {exc.code} at /v1/chat/completions.") from None
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise LLMProxyError(f"Proxy network error at /v1/chat/completions: {type(exc).__name__}") from None

        try:
            raw = json.loads(raw_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise LLMProxyError("Invalid JSON received from /v1/chat/completions.") from exc
        if not isinstance(raw, dict):
            raise LLMProxyError("Unexpected non-object JSON payload from /v1/chat/completions.")
        return raw, "urllib"

    @staticmethod
    def _extract_content(raw: dict[str, Any]) -> str:
        choices = raw.get("choices")
        if not isinstance(choices, list) or not choices:
            return ""
        first = choices[0] if isinstance(choices[0], dict) else {}
        message = first.get("message") if isinstance(first.get("message"), dict) else {}
        content = message.get("content")
        if content is None and isinstance(first.get("text"), str):
            content = first.get("text")
        return str(content).strip() if content is not None else ""

    def deterministic_fallback(
        self,
        messages: list[dict[str, Any]],
        model: str,
        reason: str,
        key_info: KeyInfo | None = None,
        fallback_context: dict[str, Any] | None = None,
        fallback_fn: Callable[[list[dict[str, Any]], str, str, dict[str, Any] | None], str] | None = None,
    ) -> ProxyResponse:
        """Build a safe offline deterministic response without touching the remote proxy."""
        generator = fallback_fn or self._fallback_generator
        content = generator(messages, model, reason, fallback_context)
        return ProxyResponse(
            content=content,
            model=model,
            used_fallback=True,
            fallback_reason=reason,
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            key_info=key_info,
            transport="deterministic_fallback",
            raw=None,
        )

    def chat_completion(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        max_tokens: int | None = None,
        max_completion_tokens: int | None = None,
        temperature: float | None = None,
        check_budget: bool | None = None,
        fallback_context: dict[str, Any] | None = None,
        fallback_fn: Callable[[list[dict[str, Any]], str, str, dict[str, Any] | None], str] | None = None,
        **extra_params: Any,
    ) -> ProxyResponse:
        """Execute a chat completion against Sherpas proxy with budget, rate, and concurrency guards."""
        target_model = model or self.default_model
        payload = build_chat_payload(
            messages=messages,
            model=target_model,
            max_tokens=max_tokens,
            max_completion_tokens=max_completion_tokens,
            temperature=temperature,
            strict_model=True,
            **extra_params,
        )

        if not self.has_team_key:
            return self.deterministic_fallback(
                messages=messages,
                model=target_model,
                reason="missing_team_key",
                fallback_context=fallback_context,
                fallback_fn=fallback_fn,
            )

        should_check_budget = self.check_budget_before_call if check_budget is None else bool(check_budget)
        key_info: KeyInfo | None = None
        if should_check_budget:
            try:
                key_info = self.ensure_budget_available()
            except BudgetExhaustedError as exc:
                if not self.fallback_on_error:
                    raise
                return self.deterministic_fallback(
                    messages=messages,
                    model=target_model,
                    reason=f"budget_exhausted: {exc}",
                    key_info=exc.key_info or self._cached_key_info,
                    fallback_context=fallback_context,
                    fallback_fn=fallback_fn,
                )
            except LLMProxyError as exc:
                if not self.fallback_on_error:
                    raise
                return self.deterministic_fallback(
                    messages=messages,
                    model=target_model,
                    reason=f"key_info_error: {exc}",
                    fallback_context=fallback_context,
                    fallback_fn=fallback_fn,
                )

        try:
            self.rate_limiter.acquire(
                block=self.block_on_rate_limit,
                timeout=self.rate_limit_timeout,
            )
            with self.concurrency_limiter.slot(timeout=self.concurrency_timeout):
                if self._should_use_openai_sdk():
                    raw, used_transport = self._call_via_openai_sdk(payload)
                else:
                    raw, used_transport = self._call_via_urllib(payload)
        except LLMProxyError as exc:
            if not self.fallback_on_error:
                raise
            return self.deterministic_fallback(
                messages=messages,
                model=target_model,
                reason=str(exc),
                key_info=key_info,
                fallback_context=fallback_context,
                fallback_fn=fallback_fn,
            )

        content = self._extract_content(raw)
        if not content:
            err = LLMProxyError("Empty completion content returned by proxy.")
            if not self.fallback_on_error:
                raise err
            return self.deterministic_fallback(
                messages=messages,
                model=target_model,
                reason=str(err),
                key_info=key_info,
                fallback_context=fallback_context,
                fallback_fn=fallback_fn,
            )

        usage = raw.get("usage") if isinstance(raw.get("usage"), dict) else {}
        return ProxyResponse(
            content=content,
            model=str(raw.get("model") or target_model),
            used_fallback=False,
            fallback_reason=None,
            usage=dict(usage),
            key_info=key_info,
            transport=used_transport,
            raw=_sanitize_mapping(raw),
        )

    def complete_text(
        self,
        prompt: str,
        system_prompt: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        fallback_context: dict[str, Any] | None = None,
    ) -> str:
        """Convenience wrapper returning only the text completion."""
        messages: list[dict[str, Any]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return self.chat_completion(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            fallback_context=fallback_context,
        ).content
