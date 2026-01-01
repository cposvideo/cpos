

import random
import os


class DeterminismController:
    """
    Enforces deterministic runtime behavior.
    """

    def apply(self, seed: int) -> None:
        os.environ["PYTHONHASHSEED"] = str(seed)
        random.seed(seed)
