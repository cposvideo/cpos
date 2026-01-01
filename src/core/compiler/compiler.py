from src.core.dag.verification import verify_dag
from src.core.runtime.determinism import DeterminismController


class CompilerOutput:
    def __init__(self, dag):
        self.dag = dag


class ContentCompiler:
    """
    Pipeline-as-Compiler core.
    Validates DAG, enforces determinism, and emits a compiled plan.
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.determinism = DeterminismController()

    def compile(self, context):
        # Enforce determinism
        self.determinism.apply(self.seed)

        # Verify DAG correctness
        verify_dag(context.dag)

        # Emit compiled output
        return CompilerOutput(context.dag)
