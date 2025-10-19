import hashlib
from dataclasses import dataclass


@dataclass
class ABPolicy:
    v1_weight: float = 0.5  # 0..1
    sticky: bool = True


class ABTestController:
    def __init__(self, policy: ABPolicy | None = None):
        self.policy = policy or ABPolicy()

    def _hash_to_unit(self, key: str) -> float:
        h = hashlib.md5(key.encode()).hexdigest()
        return int(h, 16) / float(16**32)

    def pick_arm(self, partner_id: str | None, app_id: str | None) -> str:
        if not self.policy.sticky:
            from random import random
            return "v1" if random() < self.policy.v1_weight else "v2"
        key = f"{partner_id or ''}:{app_id or ''}"
        u = self._hash_to_unit(key)
        return "v1" if u < self.policy.v1_weight else "v2"