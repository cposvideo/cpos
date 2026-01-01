from src.core.runtime.guards import RuntimeCapabilities

caps = RuntimeCapabilities({"read"})

try:
    caps.require("write")
    print("FAIL")
except Exception as e:
    print("Blocked as expected:", e)
