from typing import Dict, List, Tuple
from src.core.dag.node import DAGNode

class DAG:
    def __init__(self): self.nodes: Dict[str,DAGNode]={}; self._edges: List[Tuple[str,str]]=[]
    def add_node(self,n:DAGNode):
        if n.node_id in self.nodes: raise ValueError('dup')
        self.nodes[n.node_id]=n
        for d in n.dependencies: self._edges.append((d,n.node_id))
    def edges(self): return list(self._edges)
