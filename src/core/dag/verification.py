from src.core.dag.graph import DAG


class DAGVerificationError(Exception):
    pass


def verify_dag(dag: DAG) -> None:
    """
    Verifies that the DAG is acyclic and all dependencies exist.
    """

    visited = set()
    stack = set()

    def visit(node_id: str):
        if node_id in stack:
            raise DAGVerificationError(f"Cycle detected at node '{node_id}'")

        if node_id in visited:
            return

        stack.add(node_id)

        node = dag.nodes.get(node_id)
        if node is None:
            raise DAGVerificationError(f"Missing DAG node '{node_id}'")

        for dep in node.dependencies:
            if dep not in dag.nodes:
                raise DAGVerificationError(
                    f"Node '{node_id}' depends on missing node '{dep}'"
                )
            visit(dep)

        stack.remove(node_id)
        visited.add(node_id)

    for nid in dag.nodes:
        visit(nid)
