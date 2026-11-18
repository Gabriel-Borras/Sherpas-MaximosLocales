"""Cliente HTTP Streamable MCP y fuentes locales/semilla para casos Sherpas."""
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json
import os
import copy
from pathlib import Path
import socket
from typing import Any, Optional


class MCPClientError(Exception):
    """Error general del cliente MCP."""


class MCPAuthError(MCPClientError):
    """El servidor rechazó la autenticación."""


class MCPTransportError(MCPClientError):
    """Error de transporte o protocolo remoto."""


class CaseNotFoundError(LookupError):
    """No existe el caso solicitado."""


class InvalidSectionError(ValueError):
    """La sección solicitada no es válida."""


REPO_ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = REPO_ROOT / "cases"
SECTIONS = ("financial-health", "investment-analysis", "persona")


def load_env_file(path: Optional[str] = None) -> None:
    """Carga pares KEY=VALUE sencillos, sin reemplazar el entorno existente."""
    env_path = Path(path) if path else REPO_ROOT / ".env"
    try:
        lines = env_path.read_text(encoding="utf-8-sig").splitlines()
    except OSError:
        return
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        if key and key not in os.environ:
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            os.environ[key] = value


# Datos seed: únicamente cifras y hechos consignados en la Biblia Final V1.
_SEED = {
    "michael-carter": {
        "financial-health": {
            "case_id": "michael-carter", "name": "Michael Carter", "age": 37,
            "household_type": "SINGLE", "location": "Austin, TX", "income": 180000,
            "score": {"overall": 26, "status": "critical", "pillars": [
                {"name": "Savings & cash flow", "score": 0, "max": 25},
                {"name": "Debt", "score": 8, "max": 10},
                {"name": "Investments", "score": 11, "max": 25},
                {"name": "Liquidity", "score": 4, "max": 20},
                {"name": "Protection", "score": 4, "max": 20}],
                "top_moves": [
                    {"id": "umbrella_1m", "action": "Add $1M umbrella cover", "score_before": 26, "score_after": 31, "year": 2026},
                    {"id": "growth_allocation", "action": "Raise growth allocation 74% -> 88%", "amount_moved": 19900, "score_before": 26, "score_after": 31, "year": 2026},
                    {"id": "retire_58_lower_draw", "action": "Retire at 58 / cut withdrawals to $10,300/yr", "score_before": 26, "score_after": 62, "year": 2047}],
                "combined_moves": []},
            "key_metrics": {"savings_rate_pct": 23.9, "annual_savings": 43000, "bank_cash": 27000, "amex_balance": 3500, "amex_apr_pct": 20.0, "retirement_age": 58, "retirement_gap": 1177586, "current_draw_rate_pct": 5.6, "current_annual_draw": 59613, "target_annual_draw": 10300, "cash_months_after_2027_home": 0,
                "facts": ["Savings rate 23.9% ($43,000/yr)", "Amex $3,500 at 20% APR vs $27,000 bank cash", "2027 $550,000 home ($113,300 down): investable_assets $178,717 -> $81,172 (0 months cash)", "Rent $2,800/mo vs mortgage $3,015/mo omits $5,665/yr taxes, $2,832.50/yr insurance, $9,464 closing", "2075 (age 86): -$38,276 investable_assets despite $2,570,000 net_worth"]},
            "projections": {"yearly": [{"year": 2026, "age": 37, "investable_assets": 178717}, {"year": 2027, "age": 38, "investable_assets": 81172}, {"year": 2032, "age": 43, "investable_assets": 279056}, {"year": 2038, "age": 49, "investable_assets": 763133}, {"year": 2044, "age": 55, "investable_assets": 1550861}, {"year": 2050, "age": 61, "investable_assets": 1823675}, {"year": 2056, "age": 67, "investable_assets": 1125478}, {"year": 2062, "age": 73, "investable_assets": 717522}, {"year": 2068, "age": 79, "investable_assets": 316843}, {"year": 2074, "age": 85, "investable_assets": 3288}, {"year": 2075, "age": 86, "investable_assets": -38276, "net_worth": 2570000}, {"year": 2080, "age": 91, "investable_assets": -160752}]},
            "goals": {"chartGoals": [{"year": 2027, "month": 1, "name": "Home purchase $550,000", "down_payment": 113300, "mortgage_monthly": 3015}, {"year": 2047, "age": 58, "name": "Retire at 58"}]},
            "savingsWaterfall": {"steps": [{"step": 1, "day": 0, "owner": "Michael", "action": "Pay off $3,500 Amex (20% APR) from $27,000 bank cash", "amount": 3500, "apr_pct": 20.0}, {"step": 2, "day": 30, "owner": "Michael", "action": "Raise 401(k) deferral (+$7,500 margin)", "amount": 7500, "tax_savings_annual": 1800}]}
        },
        "investment-analysis": {"taxDragAnalysis": {"JNK": {"annual_tax_drag": 527}}, "holdings": [{"ticker": "JNK", "annual_tax_drag": 527}], "allocation": {"current_growth_pct": 74, "target_growth_pct": 88, "amount_moved": 19900}, "analysis": {"period": "2023-2026", "event_count": 11, "max_drawdown_pct": -10.2, "recovery_days": 62, "events": [{"name": "August 2024 correction", "period": "2024-08"}, {"name": "DeepSeek shock", "period": "2025-01"}, {"name": "April 2025 tariffs shock", "period": "2025-04"}], "perEventDrawdowns": [{"max_drawdown_pct": -10.2, "recovery_days": 62}]}},
        "persona": "# Michael Carter\nD5: SINGLE\n\n## Objective concerns\n- O1 Retirement shortfall\n- O2 Cash for the home purchase\n- O3 Life insurance gap: $720,000\n- O4 No umbrella cover\n\nSubjective concerns: None recorded\n\n## Tensions\nT1: Strong savings rate alongside a critical overall score.\nT2: Amex debt at 20% APR despite available bank cash.\nT3: Home purchase reduces investable assets and leaves no cash months.\nT4: Current draw rate exceeds the target annual draw.\nT5: Positive net worth while investable assets become negative.\n\n## Transition alerts\nJan 2027: $550,000 home purchase has additional taxes, insurance, and closing costs."
    },
    "samantha-lewis": {
        "financial-health": {"case_id": "samantha-lewis", "name": "Samantha Lewis", "age": 47, "household_type": "SINGLE", "children_ages": [18, 16], "score": {"overall": 82, "status": "strong", "pillars": [{"name": "Savings & cash flow", "score": None, "max": 25}, {"name": "Debt", "score": None, "max": 10}, {"name": "Investments", "score": None, "max": 25}, {"name": "Liquidity", "score": None, "max": 20}, {"name": "Protection", "score": None, "max": 20}], "top_moves": [{"id": "home_insurance", "action": "Home insurance policy", "score_before": 82, "score_after": 84, "year": 2026}, {"id": "vti_concentration", "action": "Reduce VTI concentration 39% -> 25%", "score_before": 82, "score_after": 83, "year": 2026}, {"id": "growth_adjustment", "action": "Adjust growth allocation 85% -> 80%", "score_before": 82, "score_after": 83, "year": 2026}], "combined_moves": []}, "key_metrics": {"retirement_accounts_balance": 0, "home_value": 900000, "net_worth": 1390000, "college_per_child": 50000, "college_total": 100000, "planned_home_2030": 500000, "k401_margin": 24500, "hsa_margin": 4400, "facts": ["Score 82 strong hides $0 in retirement accounts", "$900,000 home within $1.39M net worth", "2027-2030: $50,000/child university ($100,000) + $500,000 home in 2030", "2053 (age 74): -$227,414 investable_assets; net_worth < 0 in 2070"]}, "projections": {"yearly": [{"year": 2026, "age": 47, "net_worth": 1390000}, {"year": 2030, "age": 51}, {"year": 2053, "age": 74, "investable_assets": -227414}, {"year": 2070, "age": 91, "net_worth_negative": True}]}, "goals": {"chartGoals": [{"year": 2027, "year_end": 2030, "name": "University ($50,000 per child = $100,000)"}, {"year": 2030, "name": "Home purchase $500,000"}]}, "savingsWaterfall": {"steps": [{"step": 1, "day": 0, "owner": "Samantha", "action": "Confirm home policy and Porsche Cayenne insurance"}, {"step": 2, "day": 30, "owner": "Samantha", "action": "Contribute $24,500 to 401(k) + $4,400 to HSA", "k401_amount": 24500, "hsa_amount": 4400}]}},
        "investment-analysis": {"taxDragAnalysis": {"taxable_account": {"annual_tax_drag": 3032}}, "holdings": [{"ticker": "VTI", "weight_pct": 39, "target_weight_pct": 25}], "allocation": {"current_growth_pct": 85, "target_growth_pct": 80}, "analysis": {"period": "2023-2026", "event_count": 11, "events": [{"name": "August 2024 correction", "period": "2024-08"}, {"name": "DeepSeek shock", "period": "2025-01"}, {"name": "April 2025 tariffs shock", "period": "2025-04"}], "perEventDrawdowns": []}},
        "persona": "# Samantha Lewis\nD5: SINGLE\n\n## Objective concerns\nO1..O8\n\nSubjective concerns: None recorded\n\n## Tensions\nT1..T5\n\n## Transition alerts\nUniversity costs from 2027 through 2030 and a $500,000 home purchase in 2030."
    },
    "timothy-melanie-weah": {
        "financial-health": {"case_id": "timothy-melanie-weah", "name": "Timothy & Melanie Weah", "ages": [40, 38], "household_type": "DUAL", "children_ages": [6, 3], "score": {"overall": 60, "status": "vulnerable", "pillars": [{"name": "Savings & cash flow", "score": None, "max": 25}, {"name": "Debt", "score": None, "max": 10}, {"name": "Investments", "score": None, "max": 25}, {"name": "Liquidity", "score": None, "max": 20}, {"name": "Protection", "score": None, "max": 20}], "combined_target_score": 78, "top_moves": [{"id": "pay_18k_card", "action": "Pay off $18,000 credit card at 18% APR", "score_before": 60, "score_after": 62, "year": 2026}, {"id": "life_and_umbrella", "action": "Add $1.1M life insurance + $1M umbrella", "life_coverage": 1100000, "umbrella_coverage": 1000000, "year": 2026}], "combined_moves": [{"action": "Combined cordada actions", "score_before": 60, "score_after": 78}]}, "key_metrics": {"cash_balance": 150800, "cash_yield_pct": 0.09, "cash_annual_yield": 135, "credit_card_balance": 18000, "credit_card_apr_pct": 18.0, "annual_interest_cost": 3240, "life_insurance_gap": -1100000, "umbrella_coverage": 0, "k401_tax_savings_annual": 5760, "facts": ["$150,800 cash at 0.09% (~$135/yr) vs $18,000 card at 18% APR ($3,240/yr)", "Life gap -$1.1M + $0 umbrella", "2079: $16.1M investable_assets (no bankruptcy in yearly)"]}, "projections": {"yearly": [{"year": 2026, "ages": [40, 38]}, {"year": 2079, "investable_assets": 16100000, "bankruptcy": False}]}, "goals": {"chartGoals": [{"year": 2026, "name": "Pay $18k card + $1.1M life + $1M umbrella"}]}, "savingsWaterfall": {"steps": [{"step": 1, "day": 3, "owner": "Melanie", "action": "Pay off $18,000 card (18% APR) from excess cash", "amount": 18000, "apr_pct": 18.0}, {"step": 2, "day": 14, "owner": "Timothy", "action": "Reduce 3x leveraged UPRO exposure"}, {"step": 3, "day": 30, "owner": "Timothy", "action": "Activate 401(k) ($5,760/yr tax savings) + 529", "tax_savings_annual": 5760}]}},
        "investment-analysis": {"taxDragAnalysis": {}, "holdings": [{"ticker": "UPRO", "leverage": "3x"}], "allocation": {"cash_balance": 150800, "cash_yield_pct": 0.09}, "analysis": {"period": "2023-2026", "event_count": 11, "upro_volatility_warning": "3x volatility risk on UPRO vs 2023-2026 shocks", "events": [{"name": "August 2024 correction", "period": "2024-08"}, {"name": "DeepSeek shock", "period": "2025-01"}, {"name": "April 2025 tariffs shock", "period": "2025-04"}], "perEventDrawdowns": []}},
        "persona": "# Timothy & Melanie Weah\nD4: MISALIGNED (Timothy Growth 4 vs Melanie Moderate 3)\nD5: DUAL\nD6\n\nSubjective concerns: None recorded\n\n## Tensions\nT1..T5"
    },
    "daniel-emily-johnson": {
        "financial-health": {"case_id": "daniel-emily-johnson", "name": "Daniel & Emily Johnson", "ages": [44, 42], "household_type": "DUAL", "children_ages": [11, 9], "score": {"overall": 52, "status": "vulnerable", "pillars": [{"name": "Savings & cash flow", "score": None, "max": 25}, {"name": "Debt", "score": None, "max": 10}, {"name": "Investments", "score": None, "max": 25}, {"name": "Liquidity", "score": None, "max": 20}, {"name": "Protection", "score": 0, "max": 20}], "combined_target_score": 60, "top_moves": [{"id": "life_insurance", "action": "Increase life insurance +$1.166M", "amount": 1166000, "score_before": 52, "score_after": 57, "year": 2026}, {"id": "umbrella_1m", "action": "Add $1M umbrella cover", "amount": 1000000, "score_before": 52, "score_after": 56, "year": 2026}, {"id": "redirect_cash_flow", "action": "Redirect $15,032/yr cash flow", "amount": 15032, "score_before": 52, "score_after": 55, "year": 2026}], "combined_moves": [{"action": "Combined cordada actions", "score_before": 52, "score_after": 60}]}, "key_metrics": {"protection_score": "0/20", "cash_months": 1.4, "home_value": 750000, "home_equity": 190000, "life_insurance_gap": -2350000, "credit_card_balance": 18000, "credit_card_apr_pct": 24.9, "annual_savings": 26000, "annual_529_contribution": 8000, "annual_401k_contribution": 0, "potential_401k_tax_savings": 11760, "redirectable_cash_flow": 15032, "facts": ["Protection 0/20 with -$2.35M total life insurance gap", "Cash 1.4 months; $750k home vs $190k equity", "$18,000 credit card at 24.9% APR", "$26,000/yr savings and $8,000/yr 529 with $0 to 401(k) ($11,760/yr potential tax savings)"]}, "projections": {"yearly": [{"year": 2026, "ages": [44, 42]}]}, "goals": {"chartGoals": [{"year": 2026, "name": "Life +$1.166M, umbrella $1M, pay 24.9% card"}]}, "savingsWaterfall": {"steps": [{"step": 1, "day": 3, "owner": "Daniel & Emily", "action": "Pause brokerage/529 diversion to pay $18,000 card (24.9% APR) and quote life insurance", "amount": 18000, "apr_pct": 24.9}, {"step": 2, "day": 30, "owner": "Daniel & Emily", "action": "Activate 401(k) contributions ($0 current, $11,760/yr potential tax savings)", "tax_savings_annual": 11760}]}},
        "investment-analysis": {"taxDragAnalysis": {}, "holdings": [], "allocation": {}, "analysis": {"period": "2023-2026", "event_count": 11, "events": [{"name": "August 2024 correction", "period": "2024-08"}, {"name": "DeepSeek shock", "period": "2025-01"}, {"name": "April 2025 tariffs shock", "period": "2025-04"}], "perEventDrawdowns": []}},
        "persona": "# Daniel & Emily Johnson\nD4: MISALIGNED\nD5: DUAL\nD6\n\nSubjective concerns: None recorded\n\n## Tensions\nT1..T5"
    }
}


def _parse_response(body: bytes, content_type: str, request_id: Any):
    text = body.decode("utf-8", errors="replace")
    if "text/event-stream" not in content_type.lower():
        try:
            return json.loads(text) if text.strip() else None
        except json.JSONDecodeError as exc:
            raise MCPTransportError("Respuesta JSON inválida") from exc
    messages, data = [], []
    for line in text.splitlines() + [""]:
        if not line:
            if data:
                payload = "\n".join(data)
                if payload != "[DONE]":
                    try: messages.append(json.loads(payload))
                    except json.JSONDecodeError: pass
            data = []
        elif line.startswith(":"):
            continue
        elif line.startswith("data:"):
            data.append(line[5:].lstrip())
    for message in messages:
        if isinstance(message, dict) and message.get("id") == request_id:
            return message
    if messages:
        return messages[-1]
    raise MCPTransportError("SSE sin respuesta JSON-RPC")


class SherpasMCPClient:
    def __init__(self, mcp_url=None, mcp_token=None, cases_dir=None, allow_fallback=True, timeout=5, env_file=None):
        # Explicit token, including empty string, disables .env token loading.
        if mcp_url is None or cases_dir is None or mcp_token is None:
            load_env_file(env_file)
        if mcp_token is None:
            mcp_token = os.environ.get("MCP_TOKEN")
        else:
            mcp_token = str(mcp_token)
        self.url = mcp_url or os.environ.get("MCP_URL", "https://mcp-hackathon.sherpaswealth.com/mcp")
        self.token = mcp_token or ""
        self.cases_dir = Path(cases_dir) if cases_dir is not None else Path(os.environ.get("SHERPAS_CASES_DIR") or os.environ.get("CASES_DIR") or CASES_DIR)
        self.allow_fallback, self.timeout = allow_fallback, timeout
        self.session_id = None
        self._rpc_id = 0
        self._initialized = False
        self.last_source = None
        self.last_fallback_reason = None

    def _post(self, payload, expect_response=True):
        headers = {"Content-Type":"application/json", "Accept":"application/json, text/event-stream"}
        if self.token: headers["Authorization"] = "Bearer " + self.token
        if self.session_id: headers["Mcp-Session-Id"] = self.session_id
        request = Request(self.url, data=json.dumps(payload).encode(), headers=headers, method="POST")
        try:
            with urlopen(request, timeout=self.timeout) as response:
                sid = response.headers.get("Mcp-Session-Id")
                if sid: self.session_id = sid
                body = response.read()
                if not expect_response or not body: return None
                return _parse_response(body, response.headers.get("Content-Type", "application/json"), payload.get("id"))
        except HTTPError as exc:
            if exc.code in (401,403): raise MCPAuthError("MCP rechazó la autenticación (HTTP %s)" % exc.code) from exc
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code in (400, 404):
                raise MCPTransportError("HTTP %s: %s" % (exc.code, detail)) from exc
            raise MCPTransportError("Error HTTP MCP: %s" % exc.code) from exc
        except (TimeoutError, socket.timeout) as exc:
            raise MCPTransportError("Timeout al conectar con MCP") from exc
        except URLError as exc:
            if isinstance(exc.reason, (TimeoutError, socket.timeout)): raise MCPTransportError("Timeout al conectar con MCP") from exc
            raise MCPTransportError("Error de red MCP: %s" % exc.reason) from exc
        except OSError as exc:
            raise MCPTransportError("Error de transporte MCP: %s" % exc) from exc

    def _rpc(self, method, params=None):
        self._rpc_id += 1
        rid = self._rpc_id
        response = self._post({"jsonrpc":"2.0","id":rid,"method":method,"params":params or {}})
        if not isinstance(response, dict): raise MCPTransportError("Respuesta MCP vacía o inválida")
        if response.get("error"):
            err = response["error"]
            raise MCPClientError("MCP %s: %s" % (err.get("code"), err.get("message", "error")))
        return response.get("result")

    def _initialize(self):
        result = self._rpc("initialize", {"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"sherpas-backend","version":"1.0"}})
        self._post({"jsonrpc":"2.0","method":"notifications/initialized"}, expect_response=False)
        self._initialized = True
        return result

    def _tool(self, name, arguments=None, retry=True):
        if not self.token: raise MCPAuthError("MCP_TOKEN ausente")
        if not self._initialized: self._initialize()
        try:
            result = self._rpc("tools/call", {"name":name,"arguments":arguments or {}})
        except MCPTransportError as exc:
            message = str(exc).lower()
            if retry and ("session" in message or "expired" in message or "http 404" in message):
                self.session_id = None
                self._initialized = False
                self._initialize()
                return self._tool(name, arguments, retry=False)
            raise
        except MCPClientError as exc:
            message = str(exc).lower()
            if retry and ("session" in message or "initialize" in message):
                self.session_id = None
                self._initialized = False
                self._initialize()
                return self._tool(name, arguments, retry=False)
            raise
        if isinstance(result, dict) and result.get("isError"):
            content = result.get("content", [])
            message = " ".join(item.get("text", "") for item in content if isinstance(item, dict))
            raise MCPClientError(message or "Error de herramienta MCP")
        return result

    @staticmethod
    def _unwrap(result, expect_json=True):
        if isinstance(result, dict) and "structuredContent" in result: return result["structuredContent"]
        if isinstance(result, dict) and isinstance(result.get("content"), list):
            texts = [item.get("text", "") for item in result["content"]
                     if isinstance(item, dict) and item.get("type") == "text"]
            if texts:
                combined = "\n".join(texts)
                if not expect_json:
                    try:
                        value = json.loads(combined)
                        if isinstance(value, dict):
                            return next((value[key] for key in ("persona", "content", "markdown") if key in value), combined)
                        if isinstance(value, str):
                            return value
                    except json.JSONDecodeError:
                        pass
                    return combined
                try: return json.loads(combined)
                except json.JSONDecodeError: return combined
        if not expect_json and isinstance(result, dict):
            for key in ("persona", "content", "markdown"):
                if isinstance(result.get(key), str): return result[key]
        return result

    def _fallback_or_raise(self, error):
        reason = "mcp_error"
        if isinstance(error, MCPAuthError): reason = "http_401" if "401" in str(error) else ("http_403" if "403" in str(error) else "missing_token")
        elif isinstance(error, MCPTransportError): reason = "timeout" if "timeout" in str(error).lower() else "transport_error"
        if not self.allow_fallback: raise error
        self.last_fallback_reason = reason
        return None

    def _local(self, case_id):
        folder = self.cases_dir / case_id
        if not folder.is_dir(): return None
        data = {"case_id":case_id,"id":case_id,"source":"local"}
        for section, filename in zip(SECTIONS, ("financial-health.json","investment-analysis.json","persona.md")):
            path = folder / filename
            if not path.is_file(): continue
            raw = path.read_text(encoding="utf-8-sig")
            if section == "persona": data[section] = raw
            else:
                try: data[section] = json.loads(raw)
                except json.JSONDecodeError: raise MCPTransportError("JSON local inválido: %s" % path)
        seed = self._seed_case(case_id)
        if seed:
            for section in SECTIONS:
                data.setdefault(section, copy.deepcopy(seed[section]))
        return data if any(k in data for k in SECTIONS) else None

    def _seed_case(self, case_id):
        item = _SEED.get(case_id)
        if item is None:
            return None
        return {"case_id": case_id, "id": case_id, "source": "seed",
                **copy.deepcopy(item)}

    def _case_data(self, case_id, section=None):
        try:
            args = {"case_id": case_id}
            if section is not None:
                args["section"] = section
            result = self._unwrap(self._tool("get_case", args), expect_json=section != "persona")
            if section is not None and not isinstance(result, dict):
                result = {section: result}
            if isinstance(result, dict):
                if section is not None and section not in result:
                    result = {section: result}
                result = dict(result)
                result.setdefault("case_id", case_id)
                result.setdefault("id", case_id)
                result["source"] = "mcp"
                return result
            raise MCPTransportError("Respuesta inválida para get_case")
        except MCPClientError as exc:
            if section is None and ("-32602" in str(exc) or "section" in str(exc).lower()):
                merged = {"case_id":case_id,"id":case_id,"source":"mcp"}
                try:
                    for requested_section in SECTIONS:
                        merged[requested_section] = self._unwrap(
                            self._tool("get_case", {"case_id": case_id, "section": requested_section}),
                            expect_json=requested_section != "persona")
                except MCPClientError as fallback_error:
                    self._fallback_or_raise(fallback_error)
                else:
                    return merged
            self._fallback_or_raise(exc)
        local = self._local(case_id)
        if local is not None:
            self.last_source = "local"
            return local
        seed = self._seed_case(case_id)
        if seed is not None:
            self.last_source = "seed"
            return seed
        raise CaseNotFoundError("Caso no encontrado: %s" % case_id)

    def list_cases(self):
        self.last_fallback_reason = None
        try:
            result = self._unwrap(self._tool("list_cases"))
            if isinstance(result, dict): result = result.get("cases", result.get("items", []))
            if not isinstance(result, list): raise MCPTransportError("Respuesta inválida para list_cases")
            normalized = []
            for item in result:
                if isinstance(item, str): item = {"id": item}
                if not isinstance(item, dict): continue
                item = dict(item)
                item.setdefault("id", item.get("case_id"))
                if item.get("id") is None: continue
                item["source"] = "mcp"
                normalized.append(item)
            self.last_source = "mcp"
            return normalized
        except MCPClientError as exc:
            self._fallback_or_raise(exc)
        cases = []
        for folder in sorted(self.cases_dir.iterdir()) if self.cases_dir.is_dir() else []:
            data = self._local(folder.name)
            if data:
                fh = data.get("financial-health", {})
                score = fh.get("score")
                status = fh.get("status")
                if isinstance(score, dict):
                    status = score.get("status", status)
                    score = score.get("overall")
                cases.append({"id":folder.name,"name":fh.get("name",folder.name),"score":score,"status":status,"household_type":fh.get("household_type"),"source":"local"})
        if cases:
            self.last_source = "local"
            return cases
        self.last_source = "seed"
        return [{"id": cid, "name": value["financial-health"]["name"],
                 "score": value["financial-health"]["score"]["overall"],
                 "status": value["financial-health"]["score"]["status"],
                 "household_type": value["financial-health"]["household_type"],
                 "source": "seed"} for cid, value in _SEED.items()]

    def get_case(self, case_id, section=None):
        if not isinstance(case_id, str) or not case_id or ".." in case_id or "/" in case_id or "\\" in case_id:
            raise ValueError("case_id inválido")
        if section is not None:
            section = section.replace("_", "-") if isinstance(section,str) else section
            if section not in SECTIONS: raise InvalidSectionError("Sección inválida: %r" % section)
        self.last_fallback_reason = None
        data = self._case_data(case_id, section=section)
        self.last_source = data.get("source", self.last_source)
        if section is None: return copy.deepcopy(data)
        if section not in data: raise CaseNotFoundError("Caso/sección no encontrado: %s/%s" % (case_id,section))
        return copy.deepcopy(data[section])


def list_cases(*args, **kwargs):
    return SherpasMCPClient(*args, **kwargs).list_cases()


def get_case(case_id, section=None, *args, **kwargs):
    return SherpasMCPClient(*args, **kwargs).get_case(case_id, section)
