from typing import List, Dict, Any
from app.models.schemas import Neighbor
from app.utils.logging import get_logger
import pickle
import os


logger = get_logger(__name__)


class SimilarityService:
    def __init__(self, embeddings_store):
        self.embeddings_store = embeddings_store
        try:
            self._app_metadata = self._load_metadata()
        except Exception as e:
            logger.error(f"Failed to load metadata: {str(e)}")
            self._app_metadata = {}

    def _load_metadata(self):
        """
        Load app metadata mapping.

        Returns:
            Dict mapping app_id to metadata

        Raises:
            FileNotFoundError: If metadata file doesn't exist
            pickle.UnpicklingError: If metadata file is corrupted
        """
        metadata_path = 'data/app_metadata.pkl'
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'rb') as f:
                    metadata = pickle.load(f)
                logger.info(f"Loaded metadata for {len(metadata)} apps")
                return metadata
            except (pickle.UnpicklingError, EOFError) as e:
                logger.error(f"Failed to unpickle metadata file: {str(e)}")
                raise
        else:
            logger.warning(f"Metadata file not found: {metadata_path}")
            return {}

    def topk_neighbors(self, query_vec: list[float], k: int, filters: Dict[str, List[str]] | None, arm: str) -> List[Neighbor]:
        """
        Find top-k most similar apps using cosine similarity.

        Args:
            query_vec: Query embedding vector
            k: Number of neighbors to return
            filters: Optional filters for category/region
            arm: A/B test arm ('v1' or 'v2')

        Returns:
            List of Neighbor objects sorted by similarity

        Raises:
            ValueError: If inputs are invalid
            RuntimeError: If embeddings cannot be loaded
        """
        if not query_vec:
            raise ValueError("Query vector cannot be empty")

        if k <= 0:
            raise ValueError(f"k must be positive, got {k}")

        if arm not in ["v1", "v2"]:
            raise ValueError(f"arm must be 'v1' or 'v2', got {arm}")
        try:
            # Load embeddings for the specified arm (v1 or v2)
            index = self.embeddings_store.get_by_arm(arm)
            if not index:
                raise RuntimeError(f"No embeddings loaded for arm {arm}")
        except Exception as e:
            logger.error(f"Failed to load embeddings for arm {arm}: {str(e)}")
            raise RuntimeError(f"Failed to load embeddings: {str(e)}")

        # Compute cosine similarity
        from math import sqrt
        import numpy as np
        import math

        def cos(a, b):
            """Compute cosine similarity with error handling"""
            try:
                dot = sum(x*y for x,y in zip(a,b))
                na = sqrt(sum(x*x for x in a))
                nb = sqrt(sum(y*y for y in b))
                if na == 0 or nb == 0:
                    return 0.0
                return dot / (na*nb + 1e-9)
            except (ValueError, TypeError, ZeroDivisionError) as e:
                logger.warning(f"Error computing cosine similarity: {str(e)}")
                return 0.0

        items = []
        skipped_count = 0

        for app_id, embedding_array in index.items():
            try:
                vec = None

                # If the embedding is a numpy array, average it to get a single vector
                if isinstance(embedding_array, np.ndarray):
                    if len(embedding_array.shape) > 1:
                        # Multi-dimensional array: average across rows
                        vec = embedding_array.mean(axis=0).tolist()
                    else:
                        vec = embedding_array.tolist()
                elif isinstance(embedding_array, dict):
                    # Try to extract vec from dict
                    vec = embedding_array.get("vec")
                    if vec is None:
                        # If no "vec" key, skip this entry
                        skipped_count += 1
                        continue
                elif isinstance(embedding_array, (list, tuple)):
                    vec = list(embedding_array)
                else:
                    # Unknown format, skip
                    skipped_count += 1
                    continue

                # Safety check
                if vec is None or not isinstance(vec, (list, tuple)):
                    skipped_count += 1
                    continue

                # Pad or truncate vector to match query length
                if len(vec) != len(query_vec):
                    if len(vec) < len(query_vec):
                        vec = vec + [0.0] * (len(query_vec) - len(vec))
                    else:
                        vec = vec[:len(query_vec)]

                # Note: Filters are not applied in this mock implementation
                # In production, you'd load metadata and filter here

                sim = cos(query_vec, vec)
                if not math.isnan(sim) and not math.isinf(sim):
                    items.append((app_id, sim))
                else:
                    skipped_count += 1

            except Exception as e:
                logger.warning(f"Error processing embedding for app_id {app_id}: {str(e)}")
                skipped_count += 1
                continue

        if skipped_count > 0:
            logger.debug(f"Skipped {skipped_count} invalid embeddings")

        if not items:
            logger.warning("No valid embeddings found for similarity search")
            return []

        items.sort(key=lambda t: t[1], reverse=True)

        # Build neighbors with metadata
        neighbors = []
        for app_id, sim in items[:k]:
            try:
                metadata = self._app_metadata.get(app_id, {})

                # Handle NaN values from pandas
                app_name = metadata.get('name')
                category = metadata.get('category')

                # Convert NaN to None
                if app_name is not None and isinstance(app_name, float) and math.isnan(app_name):
                    app_name = None
                if category is not None and isinstance(category, float) and math.isnan(category):
                    category = None

                neighbors.append(Neighbor(
                    app_id=app_id,
                    similarity=float(sim),
                    app_name=app_name,
                    category=category
                ))
            except Exception as e:
                logger.warning(f"Error building neighbor for app_id {app_id}: {str(e)}")
                continue

        return neighbors