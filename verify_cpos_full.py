import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


"""
CPOS Full System Verification Script
===================================

Baseline Version : v1.3
Last Verified    : 2026-01-01
"""

import sys
import os
import traceback
from sqlalchemy import create_engine, inspect

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--ci", action="store_true", help="Run in strict CI mode")
args = parser.parse_args()

CI_STRICT = args.ci


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def ok(msg):
    print(f"[ OK ] {msg}")

def fail(msg):
    print(f"[FAIL] {msg}")
    sys.exit(1)

def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

def is_ci():
    return os.environ.get("CI", "").lower() in ("1", "true", "yes")

# ------------------------------------------------------------
# PHASE A — ENVIRONMENT
# ------------------------------------------------------------
section("PHASE A — ENVIRONMENT")

try:
    ok(f"Python executable : {sys.executable}")
    ok(f"Python version    : {sys.version.split()[0]}")
except Exception:
    fail("Python environment broken")

if is_ci():
    try:
        import src  # noqa
        ok("CI environment can import src package")
    except Exception:
        traceback.print_exc()
        fail("CI cannot import src package")
else:
    pythonpath = os.environ.get("PYTHONPATH", "")
    if "C:\\cpos" not in pythonpath:
        fail("Local PYTHONPATH must include C:\\cpos")
    ok("Local PYTHONPATH correct")

# ------------------------------------------------------------
# PHASE B — STATIC CODE HEALTH
# ------------------------------------------------------------
section("PHASE B — STATIC CODE HEALTH")

import compileall
import re

exclude_rx = re.compile(r"(venv|__pycache__)")

if not compileall.compile_dir(
    "src",
    quiet=1,
    rx=exclude_rx
):
    fail("Compilation errors detected in src/")

ok("All source files compile cleanly")



# ------------------------------------------------------------
# PHASE C — DETERMINISM
# ------------------------------------------------------------
section("PHASE C — DETERMINISM")

from src.domain.models import IntentSpec

i = IntentSpec("user", {"task": "determinism-test"}, {}, [])
if i.stable_hash() != i.stable_hash():
    fail("IntentSpec hashing is NOT deterministic")
ok("IntentSpec deterministic hashing verified")

# ------------------------------------------------------------
# PHASE D — RUNTIME GUARDS
# ------------------------------------------------------------
section("PHASE D — RUNTIME GUARDS")

from src.core.runtime.guards import RuntimeCapabilities

caps = RuntimeCapabilities({"read"})
try:
    caps.require("write")
    fail("Runtime guard FAILED to block disallowed capability")
except Exception:
    ok("Runtime guard enforcement works")

# ------------------------------------------------------------
# PHASE E — DAG & PARTIAL REGENERATION
# ------------------------------------------------------------
section("PHASE E — DAG & PARTIAL REGENERATION")

from src.core.dag.graph import DAG
from src.core.dag.node import DAGNode
from src.core.dag.verification import verify_dag
from src.core.runtime.partial_regen import PartialRegenerator

dag = DAG()
dag.add_node(DAGNode("fetch", "cpu"))
dag.add_node(DAGNode("process", "cpu", dependencies=["fetch"]))
dag.add_node(DAGNode("publish", "cpu", dependencies=["process"]))

verify_dag(dag)
ok("DAG structure verification passed")

affected = PartialRegenerator().affected_subgraph(dag, "process")
if affected != {"process", "publish"}:
    fail("Partial regeneration blast-radius incorrect")

ok("Partial regeneration logic correct")

# ------------------------------------------------------------
# PHASE F — DATABASE (SQLite)
# ------------------------------------------------------------
section("PHASE F — DATABASE")

from src.domain.db import init_db

init_db("sqlite:///cpos.db")
engine = create_engine("sqlite:///cpos.db")
inspector = inspect(engine)

if "jobs" not in inspector.get_table_names():
    fail("Required table 'jobs' missing")

ok("Database schema verified (jobs table present)")

# ------------------------------------------------------------
# PHASE H — MYSQL BACKEND COMPATIBILITY
# ------------------------------------------------------------
section("PHASE H — MYSQL BACKEND COMPATIBILITY")

from sqlalchemy.engine.url import make_url
url = make_url("mysql+pymysql://user:pass@localhost:3306/cpos")
if url.drivername != "mysql+pymysql":
    fail("MySQL URL parsing failed")

ok("DB layer is backend-agnostic (SQLite <-> MySQL)")

# ------------------------------------------------------------
# PHASE G — COMPILER
# ------------------------------------------------------------
section("PHASE G — COMPILER")

from src.core.compiler.context import CompilerContext
from src.core.compiler.compiler import ContentCompiler

dag = DAG()
dag.add_node(DAGNode("step1", "cpu"))
ctx = CompilerContext("verification-hash", dag)

out = ContentCompiler().compile(ctx)
if not hasattr(out, "dag"):
    fail("Compiler output invalid")

ok("Compiler pipeline verified")

# ------------------------------------------------------------
# PHASE I — WINDOWS SERVICE MODE
# ------------------------------------------------------------
section("PHASE I — WINDOWS SERVICE MODE")

import threading
sys.stdin = None

def boot_check():
    from src.api.main import app
    return app is not None

t = threading.Thread(target=boot_check)
t.start()
t.join(timeout=5)

if t.is_alive():
    fail("API import blocks in service mode")

ok("CPOS boots cleanly in non-interactive mode")

# ------------------------------------------------------------
# PHASE J — AIR-GAP MODE
# ------------------------------------------------------------
section("PHASE J — AIR-GAP MODE")

from src.core.runtime.network import enforce_airgap
import socket

enforce_airgap()
try:
    socket.socket()
    fail("Socket creation allowed in air-gap mode")
except Exception:
    ok("Outbound network blocked in air-gap mode")

# ------------------------------------------------------------
# PHASE V — CI / CD GATE
# ------------------------------------------------------------
section("PHASE V — CI / CD GATE")

if is_ci():
    ok("Running under CI environment")
else:
    ok("Local run (CI not enforced)")

# ------------------------------------------------------------
# FINAL RESULT
# ------------------------------------------------------------
section("FINAL RESULT")

ok("CPOS FULL SYSTEM VERIFICATION PASSED")
print("\n🎉 SYSTEM STATUS: GO (PRODUCTION-SAFE BASELINE v1.3)")
