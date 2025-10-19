# Module: metrics.py
"""
Metrics and instrumentation for MobUpps API
Provides request counters, latency tracking, and A/B test metrics
"""
from dataclasses import dataclass, field
from typing import Dict, List
from collections import defaultdict
from threading import Lock
import time


@dataclass
class LatencyStats:
    """Statistics for tracking latencies"""
    count: int = 0
    total_ms: float = 0.0
    min_ms: float = float('inf')
    max_ms: float = 0.0
    p50_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0
    samples: List[float] = field(default_factory=list)

    def add_sample(self, latency_ms: float) -> None:
        """Add a latency sample"""
        self.count += 1
        self.total_ms += latency_ms
        self.min_ms = min(self.min_ms, latency_ms)
        self.max_ms = max(self.max_ms, latency_ms)
        self.samples.append(latency_ms)

        # Keep only last 1000 samples for percentile calculation
        if len(self.samples) > 1000:
            self.samples.pop(0)

        # Update percentiles
        if self.samples:
            sorted_samples = sorted(self.samples)
            self.p50_ms = sorted_samples[int(len(sorted_samples) * 0.50)]
            self.p95_ms = sorted_samples[int(len(sorted_samples) * 0.95)]
            self.p99_ms = sorted_samples[int(len(sorted_samples) * 0.99)]

    @property
    def avg_ms(self) -> float:
        """Calculate average latency"""
        return self.total_ms / self.count if self.count > 0 else 0.0


class MetricsCollector:
    """
    In-memory metrics collector for API performance tracking
    Thread-safe for concurrent requests
    """

    def __init__(self):
        self._lock = Lock()

        # Request counters
        self.request_count = 0
        self.request_count_by_endpoint: Dict[str, int] = defaultdict(int)
        self.request_count_by_status: Dict[int, int] = defaultdict(int)

        # Latency tracking
        self.latencies_by_endpoint: Dict[str, LatencyStats] = defaultdict(LatencyStats)

        # A/B test metrics
        self.ab_assignments: Dict[str, int] = defaultdict(int)  # arm -> count
        self.ab_assignments_by_endpoint: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

        # Error counters
        self.error_count = 0
        self.error_count_by_type: Dict[str, int] = defaultdict(int)

        # Start time
        self.start_time = time.time()

    def record_request(self, endpoint: str, status_code: int, latency_ms: float) -> None:
        """Record an HTTP request with its metrics"""
        with self._lock:
            self.request_count += 1
            self.request_count_by_endpoint[endpoint] += 1
            self.request_count_by_status[status_code] += 1
            self.latencies_by_endpoint[endpoint].add_sample(latency_ms)

            # Track errors (4xx and 5xx)
            if status_code >= 400:
                self.error_count += 1

    def record_ab_assignment(self, endpoint: str, arm: str) -> None:
        """Record an A/B test arm assignment"""
        with self._lock:
            self.ab_assignments[arm] += 1
            self.ab_assignments_by_endpoint[endpoint][arm] += 1

    def record_error(self, error_type: str) -> None:
        """Record an error occurrence"""
        with self._lock:
            self.error_count += 1
            self.error_count_by_type[error_type] += 1

    def get_summary(self) -> Dict:
        """Get a summary of all collected metrics"""
        with self._lock:
            uptime_seconds = time.time() - self.start_time

            # Calculate latency stats per endpoint
            latencies_summary = {}
            for endpoint, stats in self.latencies_by_endpoint.items():
                latencies_summary[endpoint] = {
                    "count": stats.count,
                    "avg_ms": round(stats.avg_ms, 2),
                    "min_ms": round(stats.min_ms, 2) if stats.min_ms != float('inf') else 0,
                    "max_ms": round(stats.max_ms, 2),
                    "p50_ms": round(stats.p50_ms, 2),
                    "p95_ms": round(stats.p95_ms, 2),
                    "p99_ms": round(stats.p99_ms, 2),
                }

            # A/B test summary
            ab_summary = {
                "total_assignments": sum(self.ab_assignments.values()),
                "by_arm": dict(self.ab_assignments),
                "by_endpoint": {
                    endpoint: dict(arms)
                    for endpoint, arms in self.ab_assignments_by_endpoint.items()
                }
            }

            return {
                "uptime_seconds": round(uptime_seconds, 2),
                "requests": {
                    "total": self.request_count,
                    "by_endpoint": dict(self.request_count_by_endpoint),
                    "by_status": dict(self.request_count_by_status),
                },
                "latencies": latencies_summary,
                "ab_tests": ab_summary,
                "errors": {
                    "total": self.error_count,
                    "by_type": dict(self.error_count_by_type),
                },
            }

    def reset(self) -> None:
        """Reset all metrics (useful for testing)"""
        with self._lock:
            self.__init__()


# Global singleton instance
_metrics_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector instance"""
    return _metrics_collector


def record_request(endpoint: str, status_code: int, latency_ms: float) -> None:
    """Convenience function to record a request"""
    _metrics_collector.record_request(endpoint, status_code, latency_ms)


def record_ab_assignment(endpoint: str, arm: str) -> None:
    """Convenience function to record an A/B assignment"""
    _metrics_collector.record_ab_assignment(endpoint, arm)


def record_error(error_type: str) -> None:
    """Convenience function to record an error"""
    _metrics_collector.record_error(error_type)


def get_metrics_summary() -> Dict:
    """Convenience function to get metrics summary"""
    return _metrics_collector.get_summary()
