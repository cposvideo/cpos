class RuntimeGuardError(Exception):
    pass


class RuntimeCapabilities:
    """
    Enforces runtime capability constraints.
    """

    def __init__(self, allowed):
        self.allowed = set(allowed)

    def require(self, capability: str):
        if capability not in self.allowed:
            raise RuntimeGuardError(
                f"Capability '{capability}' is not permitted"
            )
