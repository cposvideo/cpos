from typing import Set
from src.core.dag.graph import DAG


class PartialRegenerator:
    """
    Computes the blast radius of a change in a DAG.
    Policy:
    - changed_node must exist
    - regeneration includes the node itself + all downstream dependents
    """

    def affected_subgraph(self, dag, changed_node: str):
        # ---- POLICY ENFORCEMENT ----
        if changed_node not in dag.nodes:
            raise ValueError(f"Unknown DAG node '{changed_node}'")

        # ---- BUILD REVERSE DEPENDENCY MAP ----
        reverse = {node_id: set() for node_id in dag.nodes}

        for node_id, node in dag.nodes.items():
            for dep in getattr(node, "dependencies", []):
                if dep in reverse:
                    reverse[dep].add(node_id)

        # ---- WALK DOWNSTREAM ----
        affected = set()

        def visit(node_id):
            if node_id in affected:
                return
            affected.add(node_id)
            for child in reverse.get(node_id, []):
                visit(child)

        visit(changed_node)
        return affected
