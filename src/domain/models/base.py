import json
import hashlib
from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass(frozen=True)
class IntentSpec:
    """
    Canonical CPOS Intent Specification.
    This is the collapse point for all upstream chaos (user, web, rss, api).
    """

    source_type: str
    payload: Dict[str, Any]
    constraints: Dict[str, Any] = field(default_factory=dict)
    policies: List[str] = field(default_factory=list)

    def stable_hash(self) -> str:
        """
        Deterministic, content-addressed hash.
        Any change in intent MUST change this hash.
        """
        canonical = {
            "source_type": self.source_type,
            "payload": self.payload,
            "constraints": self.constraints,
            "policies": self.policies,
        }

        encoded = json.dumps(
            canonical,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("utf-8")

        return hashlib.sha256(encoded).hexdigest()
