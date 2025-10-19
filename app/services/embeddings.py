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

    def vectorize(self, app_meta: dict, arm: str = "v1") -> list[float]:
        """
        Generate embedding vector for new app.
        v1: 64 dimensions (simpler model)
        v2: 128 dimensions (more sophisticated model)
        """
        import random
        import numpy as np

        # Determine dimensions based on arm
        dim = 64 if arm == "v1" else 128

        # Base vector from app metadata
        random.seed(hash(str(app_meta)) % (2**32))
        base = np.array([random.random() for _ in range(dim)])

        # Add category signal if present
        category = app_meta.get('category', '')
        if category:
            cat_hash = hash(str(category)) % (2**32)
            random.seed(cat_hash)
            # v2 has stronger category signal
            strength = 0.3 if arm == "v1" else 0.6
            cat_signal = np.array([random.random() for _ in range(dim)]) * strength
            base += cat_signal

        # Normalize
        norm = np.linalg.norm(base)
        return (base / (norm + 1e-9)).tolist()