from fastapi import FastAPI
from pydantic import BaseModel

# ===== Domain =====
from src.domain.models import IntentSpec, Job
from src.domain.db import get_session

# ===== Core DAG / Compiler =====
from src.core.dag.graph import DAG
from src.core.dag.node import DAGNode
from src.core.compiler.context import CompilerContext
from src.core.compiler.compiler import ContentCompiler
from src.core.runtime.partial_regen import PartialRegenerator


app = FastAPI(
    title="CPOS – Content Production Operating System",
    version="1.0.0",
)


# =========================
# Request Models
# =========================
class JobRequest(BaseModel):
    task: str


# =========================
# Health
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# Compile Job (Persisted)
# =========================
@app.post("/jobs/compile")
def compile_job(req: JobRequest):
    # 1. Build Intent
    intent = IntentSpec(
        source_type="user",
        payload={"task": req.task},
        constraints={},
        policies=[],
    )

    # 2. Build DAG (baseline single-step)
    dag = DAG()
    dag.add_node(DAGNode("step1", "cpu"))

    # 3. Compile
    ctx = CompilerContext(
        intent_hash=intent.stable_hash(),
        dag=dag,
    )

    out = ContentCompiler().compile(ctx)

    # 4. Persist Job
    session = get_session()
    job = Job(
        intent_hash=intent.stable_hash(),
        task=req.task,
        status="compiled",
    )
    session.add(job)
    session.commit()

    return {
        "job_id": job.id,
        "intent_hash": intent.stable_hash(),
        "dag_nodes": list(out.dag.nodes.keys()),
        "status": "compiled",
    }


# =========================
# Multi-Step DAG Compile
# =========================
@app.post("/jobs/compile-multistep")
def compile_multistep(req: JobRequest):
    intent = IntentSpec(
        source_type="user",
        payload={"task": req.task},
        constraints={},
        policies=[],
    )

    dag = DAG()
    dag.add_node(DAGNode("fetch", "cpu"))
    dag.add_node(DAGNode("process", "cpu", dependencies=["fetch"]))
    dag.add_node(DAGNode("publish", "cpu", dependencies=["process"]))

    ctx = CompilerContext(
        intent_hash=intent.stable_hash(),
        dag=dag,
    )

    out = ContentCompiler().compile(ctx)

    session = get_session()
    job = Job(
        intent_hash=intent.stable_hash(),
        task=req.task,
        status="compiled-multistep",
    )
    session.add(job)
    session.commit()

    return {
        "job_id": job.id,
        "intent_hash": intent.stable_hash(),
        "dag_nodes": list(out.dag.nodes.keys()),
        "status": "compiled-multistep",
    }


# =========================
# Partial Regeneration API
# =========================
@app.post("/jobs/partial-regenerate")
def partial_regenerate(node_id: str):
    dag = DAG()
    dag.add_node(DAGNode("fetch", "cpu"))
    dag.add_node(DAGNode("process", "cpu", dependencies=["fetch"]))
    dag.add_node(DAGNode("publish", "cpu", dependencies=["process"]))

    affected = PartialRegenerator().affected_subgraph(dag, node_id)

    return {
        "changed_node": node_id,
        "affected_nodes": sorted(list(affected)),
    }
