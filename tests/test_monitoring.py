from app.core.metrics import metrics_collector


def test_request_id_and_timing_headers(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert "x-request-id" in res.headers
    assert "x-process-time-ms" in res.headers


def test_detailed_health_and_metrics(client):
    metrics_collector.reset()

    client.get("/api/v1/health")
    health = client.get("/api/v1/monitoring/health/detailed")
    assert health.status_code == 200
    data = health.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert data["total_requests"] >= 1

    metrics = client.get("/api/v1/monitoring/metrics")
    assert metrics.status_code == 200
    m_data = metrics.json()
    assert m_data["total_requests"] >= 2
    assert "GET /api/v1/health" in m_data["endpoints"]

    prom = client.get("/api/v1/monitoring/metrics/prometheus")
    assert prom.status_code == 200
    assert "http_requests_total" in prom.text
    assert "football_uptime_seconds" in prom.text


def test_logs_endpoint_requires_admin(client, auth_headers):
    # Tokensiz -> 401
    assert client.get("/api/v1/monitoring/logs").status_code == 401

    # Oddiy foydalanuvchi -> 403
    viewer_headers = auth_headers("log_viewer", "viewer")
    assert client.get("/api/v1/monitoring/logs", headers=viewer_headers).status_code == 403

    # Admin -> 200 va JSON loglar ro'yxati
    admin_headers = auth_headers("log_admin", "admin")
    res = client.get("/api/v1/monitoring/logs?limit=5", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["count"] >= 1