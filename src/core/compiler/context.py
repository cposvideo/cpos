from dataclasses import dataclass
from src.core.dag.graph import DAG


@dataclass
class CompilerContext:
    intent_hash: str
    dag: DAG
