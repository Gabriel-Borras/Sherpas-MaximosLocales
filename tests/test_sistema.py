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


class SistemaAgentesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.agentes_home = Path(self.tmp.name) / "agentes"
        self.env = os.environ.copy()
        self.env["AGENTES_HOME"] = str(self.agentes_home)

    def tearDown(self):
        self.tmp.cleanup()

    def run_bin(self, name, *args):
        return subprocess.run(
            [sys.executable, str(BIN / name), *args],
            env=self.env,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_tareas_flujo_y_dependencias(self):
        r1 = self.run_bin("tareas", "add", "Base de datos", "-p", "app", "--para", "backend")
        self.assertEqual(r1.returncode, 0, r1.stderr)
        self.assertEqual(r1.stdout.strip(), "1")

        r2 = self.run_bin("tareas", "add", "UI login", "-p", "app", "--dep", "1")
        self.assertEqual(r2.returncode, 0, r2.stderr)

        # Dependencia sin cumplir y asignada a otro
        self.assertNotEqual(self.run_bin("tareas", "tomar", "2", "-p", "app", "--como", "frontend").returncode, 0)
        self.assertNotEqual(self.run_bin("tareas", "tomar", "1", "-p", "app", "--como", "frontend").returncode, 0)

        # Dueño correcto toma y cierra
        self.assertEqual(self.run_bin("tareas", "tomar", "1", "-p", "app", "--como", "backend").returncode, 0)
        self.assertNotEqual(self.run_bin("tareas", "tomar", "1", "-p", "app", "--como", "otro").returncode, 0)
        self.assertEqual(self.run_bin("tareas", "listo", "1", "-p", "app", "--nota", "ok").returncode, 0)

        # Ahora la dependiente sí se puede tomar
        self.assertEqual(self.run_bin("tareas", "tomar", "2", "-p", "app", "--como", "frontend").returncode, 0)

        # Bloquear y liberar
        self.assertEqual(self.run_bin("tareas", "bloquear", "2", "-p", "app", "--motivo", "falta token").returncode, 0)
        self.assertEqual(self.run_bin("tareas", "liberar", "2", "-p", "app").returncode, 0)
        ver = self.run_bin("tareas", "ver", "2", "-p", "app")
        self.assertEqual(json.loads(ver.stdout)["estado"], "pendiente")

    def test_equipo_cli_y_estado_local(self):
        ayuda = self.run_bin("equipo", "-h")
        self.assertEqual(ayuda.returncode, 0)
        self.assertIn("publicar", ayuda.stdout)

        sin_conf = self.run_bin("equipo", "mias")
        self.assertNotEqual(sin_conf.returncode, 0)
        self.assertIn("equipo.conf", sin_conf.stderr)

        # Probar estado_local con un repo git temporal y registro de agentes abiertos
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
        (estado_dir / "abiertos.json").write_text(json.dumps({"backend": {"workspace": 1}}), encoding="utf-8")

        os.environ["AGENTES_HOME"] = str(self.agentes_home)
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


if __name__ == "__main__":
    unittest.main()
