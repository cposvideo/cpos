from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass(frozen=True)
class DAGNode:
    node_id: str
    node_type: str
    inputs: Dict[str, Any]=field(default_factory=dict)
    resources: Dict[str, Any]=field(default_factory=dict)
    dependencies: List[str]=field(default_factory=list)
