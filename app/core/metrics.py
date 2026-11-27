import threading
import time
from collections import defaultdict


class MetricsCollector:
    """HTTP so'rovlar bo'yicha real vaqt ko'rsatkichlarini yig'uvchi yagona obyekt."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.reset()

    def reset(self) -> None:
        with self._lock:
            self._start_time = time.time()
            self._total_requests = 0
            self._status_counts: dict[str, int] = defaultdict(int)
            self._endpoint_stats: dict[str, dict[str, float | int]] = {}

    def record_request(self, method: str, path: str, status_code: int, duration_ms: float) -> None:
        key = f"{method} {path}"
        status_group = f"{status_code // 100}xx"
        with self._lock:
            self._total_requests += 1
            self._status_counts[status_group] += 1

            if key not in self._endpoint_stats:
                self._endpoint_stats[key] = {
                    "count": 0,
                    "errors": 0,
                    "total_ms": 0.0,
                    "max_ms": 0.0,
                }

            stat = self._endpoint_stats[key]
            stat["count"] = int(stat["count"]) + 1
            stat["total_ms"] = float(stat["total_ms"]) + duration_ms
            if duration_ms > float(stat["max_ms"]):
                stat["max_ms"] = round(duration_ms, 2)
            if status_code >= 400:
                stat["errors"] = int(stat["errors"]) + 1

    def get_summary(self) -> dict:
        with self._lock:
            uptime = round(time.time() - self._start_time, 2)
            endpoints = {}
            for key, stat in self._endpoint_stats.items():
                count = int(stat["count"])
                avg_ms = round(float(stat["total_ms"]) / count, 2) if count else 0.0
                endpoints[key] = {
                    "count": count,
                    "errors": int(stat["errors"]),
                    "avg_ms": avg_ms,
                    "max_ms": stat["max_ms"],
                }
            return {
                "uptime_seconds": uptime,
                "total_requests": self._total_requests,
                "status_groups": dict(self._status_counts),
                "endpoints": endpoints,
            }

    def to_prometheus(self) -> str:
        summary = self.get_summary()
        lines = [
            "# HELP football_uptime_seconds Ilovaning uzluksiz ishlash vaqti (soniya)",
            "# TYPE football_uptime_seconds gauge",
            f"football_uptime_seconds {summary['uptime_seconds']}",
            "# HELP http_requests_total Jami HTTP so'rovlar soni",
            "# TYPE http_requests_total counter",
            f"http_requests_total {summary['total_requests']}",
        ]
        for group, count in summary["status_groups"].items():
            lines.append(f'http_requests_by_status_total{{group="{group}"}} {count}')
        return "\n".join(lines) + "\n"


metrics_collector = MetricsCollector()