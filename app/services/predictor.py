from typing import List
from app.models.schemas import Neighbor, Prediction
from app.utils.logging import get_logger
import pandas as pd
import os


logger = get_logger(__name__)


class PerformancePredictor:
    def __init__(self, arm: str, performance_data: dict = None):
        """
        Initialize predictor with A/B test arm and optional cached performance data.

        Args:
            arm: A/B test arm ('v1' or 'v2')
            performance_data: Optional pre-loaded performance data dict (for caching)
        """
        if arm not in ["v1", "v2"]:
            raise ValueError(f"arm must be 'v1' or 'v2', got {arm}")
        self.arm = arm

        # Use cached data if provided, otherwise load from file
        if performance_data is not None:
            self._performance_data = performance_data
            logger.info(f"Using cached performance data ({len(performance_data)} apps)")
        else:
            try:
                self._performance_data = self._load_performance_data()
            except Exception as e:
                logger.error(f"Failed to load performance data: {str(e)}")
                self._performance_data = {}

    def _load_performance_data(self):
        """
        Load historical performance data.

        Returns:
            Dict mapping app_id to performance metrics

        Raises:
            FileNotFoundError: If performance data file doesn't exist
            pd.errors.ParserError: If CSV is malformed
        """
        perf_path = 'data/historical_performance.csv'
        if os.path.exists(perf_path):
            try:
                df = pd.read_csv(perf_path)

                # Validate required columns
                required_cols = ['app_id', 'clicks', 'impressions']
                missing_cols = [col for col in required_cols if col not in df.columns]
                if missing_cols:
                    raise ValueError(f"Missing required columns: {missing_cols}")

                # Aggregate performance metrics by app_id
                agg = df.groupby('app_id').agg({
                    'clicks': 'sum',
                    'impressions': 'sum',
                    'event_count': 'sum' if 'event_count' in df.columns else 'count',
                    'mmp_offer_default_revenue': 'mean' if 'mmp_offer_default_revenue' in df.columns else 'mean'
                }).reset_index()

                # Calculate CTR (Click-Through Rate) as performance score
                agg['ctr'] = agg['clicks'] / (agg['impressions'] + 1)

                perf_data = agg.set_index('app_id').to_dict('index')
                logger.info(f"Loaded performance data for {len(perf_data)} apps")
                return perf_data

            except pd.errors.ParserError as e:
                logger.error(f"Failed to parse performance data CSV: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"Error loading performance data: {str(e)}")
                raise
        else:
            logger.warning(f"Performance data file not found: {perf_path}")
            return {}

    def predict(self, app: dict, neighbors: List[Neighbor]) -> Prediction:
        """
        Predict performance based on similar historical apps' actual metrics.

        Args:
            app: App metadata dict
            neighbors: List of similar apps with similarity scores

        Returns:
            Prediction with score and segments

        Raises:
            ValueError: If inputs are invalid
        """
        if not neighbors:
            raise ValueError("At least one neighbor is required for prediction")

        if not isinstance(app, dict):
            raise ValueError(f"app must be a dict, got {type(app)}")

        try:
            # Get performance scores for neighbors that have data
            weighted_scores = []
            total_similarity = 0.0

            for n in neighbors[:5]:  # Top 5 neighbors
                try:
                    if n.app_id in self._performance_data:
                        perf = self._performance_data[n.app_id]
                        ctr = perf.get('ctr', 0)

                        # Validate CTR value
                        if not isinstance(ctr, (int, float)) or ctr < 0:
                            logger.warning(f"Invalid CTR value for app {n.app_id}: {ctr}")
                            continue

                        # Weight by similarity
                        weighted_scores.append(ctr * n.similarity)
                        total_similarity += n.similarity
                except Exception as e:
                    logger.warning(f"Error processing neighbor {n.app_id}: {str(e)}")
                    continue

            if weighted_scores and total_similarity > 0:
                # Average of weighted historical performance
                score = sum(weighted_scores) / max(total_similarity, 0.1)
                # Normalize to 0-1 range (CTR is typically small)
                score = min(0.95, max(0.05, score * 1000))  # Scale up CTR
                logger.debug(f"Calculated score from {len(weighted_scores)} neighbors: {score}")
            else:
                # Fallback if no performance data available
                fallback_sim = sum(n.similarity for n in neighbors[:min(5, len(neighbors))])
                score = 0.5 + (fallback_sim / min(5, len(neighbors))) * 0.4
                logger.info(f"Using fallback score calculation: {score}")

            segments = self._infer_segments(app, neighbors)
            return Prediction(score=float(round(score, 3)), segments=segments)

        except Exception as e:
            logger.error(f"Error in predict method: {str(e)}", exc_info=True)
            # Return a safe default prediction
            return Prediction(score=0.5, segments=["unknown"])

    def _infer_segments(self, app: dict, neighbors: List[Neighbor]):
        # דמו: פילוח לפי קטגוריה/תכונות אם קיימות
        segs = set()
        cat = (app.get("category") or "").lower()
        if "game" in cat or "Games" in cat:
            segs.add("gamers")
        if "fitness" in cat:
            segs.add("fitness_lovers")
        feats = set((app.get("features") or []))
        if "sharing" in feats:
            segs.add("social")
        if not segs:
            segs.add("tech-savvy")
        return sorted(list(segs))