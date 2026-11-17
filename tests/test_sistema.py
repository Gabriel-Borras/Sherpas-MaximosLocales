import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "agentes" / "bin"


def load_script(name):
    path = str(BIN / name)
    loader = importlib.machinery.SourceFileLoader(f"mod_{name}", path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


class SistemaAgentesWindowsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.agentes_home = Path(self.tmp.name) / "agentes"
        self.env = os.environ.copy()
        self.env["AGENTES_HOME"] = str(self.agentes_home)

    def tearDown(self):
        self.tmp.cleanup()

    def run_bin(self, name, *args):
        if os.name == "nt":
            cmd = [str(BIN / f"{name}.cmd"), *args]
        else:
            cmd = [sys.executable, str(BIN / name), *args]
        return subprocess.run(
            cmd,
            env=self.env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    def test_tareas_flujo_y_dependencias(self):
        r1 = self.run_bin("tareas", "add", "Base de datos", "-p", "app", "--para", "backend")
        self.assertEqual(r1.returncode, 0, r1.stderr)
        self.assertEqual(r1.stdout.strip(), "1")

        r2 = self.run_bin("tareas", "add", "UI login", "-p", "app", "--dep", "1")
        self.assertEqual(r2.returncode, 0, r2.stderr)

        self.assertNotEqual(self.run_bin("tareas", "tomar", "2", "-p", "app", "--como", "frontend").returncode, 0)
        self.assertNotEqual(self.run_bin("tareas", "tomar", "1", "-p", "app", "--como", "frontend").returncode, 0)

        self.assertEqual(self.run_bin("tareas", "tomar", "1", "-p", "app", "--como", "backend").returncode, 0)
        self.assertNotEqual(self.run_bin("tareas", "tomar", "1", "-p", "app", "--como", "otro").returncode, 0)
        self.assertEqual(self.run_bin("tareas", "listo", "1", "-p", "app", "--nota", "ok").returncode, 0)
        self.assertEqual(self.run_bin("tareas", "tomar", "2", "-p", "app", "--como", "frontend").returncode, 0)

        self.assertEqual(self.run_bin("tareas", "bloquear", "2", "-p", "app", "--motivo", "falta token").returncode, 0)
        self.assertEqual(self.run_bin("tareas", "liberar", "2", "-p", "app").returncode, 0)
        ver = self.run_bin("tareas", "ver", "2", "-p", "app")
        self.assertEqual(json.loads(ver.stdout)["estado"], "pendiente")

    def test_equipo_cli_y_estado_local(self):
        ayuda = self.run_bin("equipo", "-h")
        self.assertEqual(ayuda.returncode, 0, ayuda.stderr)
        self.assertIn("publicar", ayuda.stdout)

        sin_conf = self.run_bin("equipo", "mias")
        self.assertNotEqual(sin_conf.returncode, 0)
        self.assertIn("equipo.conf", sin_conf.stderr)

        repo_dir = Path(self.tmp.name) / "proyecto"
        repo_dir.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=repo_dir, check=True)
        (repo_dir / "a.txt").write_text("hola\n", encoding="utf-8")
        subprocess.run(["git", "add", "a.txt"], cwd=repo_dir, check=True)
        subprocess.run(
            ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "init"],
            cwd=repo_dir,
            check=True,
        )

        estado_dir = self.agentes_home / "estado"
        estado_dir.mkdir(parents=True)
        (estado_dir / "abiertos.json").write_text(json.dumps({"backend": {"dir": str(repo_dir)}}), encoding="utf-8")

        equipo = load_script("equipo")
        equipo.HOME = self.agentes_home
        equipo.CONF = self.agentes_home / "equipo.conf"
        equipo.CONF.write_text(
            f"MAQUINA=ana\nROL=orquestador\nREPO=org/proyecto\nDIR={repo_dir}\n",
            encoding="utf-8",
        )
        c = equipo.conf()
        out = equipo.estado_local(c)
        self.assertIn("<!-- equipo:estado:ana -->", out)
        self.assertIn("ana · orquestador", out)
        self.assertIn("agentes abiertos: backend", out)
        self.assertIn("init", out)

    def test_estado_y_lanzar_windows(self):
        # Preparar roles y agentes.conf dentro de AGENTES_HOME temporal
        (self.agentes_home / "roles").mkdir(parents=True)
        (self.agentes_home / "roles" / "_comun.md").write_text("comun\n", encoding="utf-8")
        (self.agentes_home / "roles" / "backend.md").write_text("rol backend\n", encoding="utf-8")
        (self.agentes_home / "agentes.conf").write_text(
            f"backend|{self.tmp.name}|roles/backend.md|model=sonnet\n",
            encoding="utf-8",
        )

        ls = self.run_bin("lanzar", "--listar")
        self.assertEqual(ls.returncode, 0, ls.stderr)
        self.assertIn("backend", ls.stdout)

        dry = self.run_bin("lanzar", "backend", "--dry-run")
        self.assertEqual(dry.returncode, 0, dry.stderr)
        self.assertTrue((self.agentes_home / "estado" / "abiertos.json").exists())

        est = self.run_bin("estado")
        self.assertEqual(est.returncode, 0, est.stderr)
        estado_md = (self.agentes_home / "estado" / "ESTADO.md").read_text(encoding="utf-8")
        self.assertIn("backend", estado_md)

        cerrar = self.run_bin("lanzar", "--cerrar", "backend")
        self.assertEqual(cerrar.returncode, 0, cerrar.stderr)


if __name__ == "__main__":
    unittest.main()
