import pickle
from functools import lru_cache
from typing import Literal


Arm = Literal["v1", "v2"]


class EmbeddingsStore:
    def __init__(self, path_v1: str, path_v2: str):
        self.path_v1 = path_v1
        self.path_v2 = path_v2
        self._v1 = None
        self._v2 = None

    @lru_cache(maxsize=1)
    def load_v1(self):
        with open(self.path_v1, "rb") as f:
            self._v1 = pickle.load(f)
        return self._v1

    @lru_cache(maxsize=1)
    def load_v2(self):
        with open(self.path_v2, "rb") as f:
            self._v2 = pickle.load(f)
        return self._v2

    def get_by_arm(self, arm: Arm):
        return self.load_v1() if arm == "v1" else self.load_v2()

    def vectorize(self, app_meta: dict) -> list[float]:
        # דמו: החזר וקטור פשוט לפי האש של שדות (בפועל: מודל/lookup)
        import random
        random.seed(hash(str(app_meta)) % (2**32))
        return [random.random() for _ in range(64)]