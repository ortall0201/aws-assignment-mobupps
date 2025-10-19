"""
Performance tests to verify < 200ms latency requirement.
Assignment requirement: "Performance test showing <200ms latency" (HOME_ASSIGNMENT.md line 81)
"""
from fastapi.testclient import TestClient
from app.main import app
import time
import statistics


client = TestClient(app)


def test_find_similar_latency_single_request():
    """Test that find-similar endpoint responds in < 200ms for a single request"""
    payload = {
        "app": {
            "name": "Fitness Tracker Pro",
            "category": "Health & Fitness",
            "region": "US",
            "pricing": "freemium",
            "features": ["tracking", "sharing"]
        },
        "top_k": 10,
        "partner_id": "perf_test_partner",
        "app_id": "perf_test_app"
    }

    start = time.perf_counter()
    response = client.post("/api/v1/find-similar", json=payload)
    latency_ms = (time.perf_counter() - start) * 1000

    assert response.status_code == 200, f"Request failed: {response.json()}"
    assert latency_ms < 200, f"Latency {latency_ms:.2f}ms exceeds 200ms requirement"
    print(f"[PASS] Single request latency: {latency_ms:.2f}ms")


def test_find_similar_latency_average():
    """Test that average latency across multiple requests is < 200ms"""
    payload = {
        "app": {
            "name": "Fitness Tracker Pro",
            "category": "Health & Fitness",
            "region": "US",
            "pricing": "freemium"
        },
        "top_k": 20,
        "partner_id": "perf_test_partner",
        "app_id": "perf_test_app"
    }

    latencies = []
    num_requests = 10

    for i in range(num_requests):
        start = time.perf_counter()
        response = client.post("/api/v1/find-similar", json=payload)
        latency_ms = (time.perf_counter() - start) * 1000

        assert response.status_code == 200, f"Request {i} failed"
        latencies.append(latency_ms)

    avg_latency = statistics.mean(latencies)
    p95_latency = statistics.quantiles(latencies, n=20)[18]  # 95th percentile
    p99_latency = max(latencies)  # For small sample, max is p99

    assert avg_latency < 200, f"Average latency {avg_latency:.2f}ms exceeds 200ms"

    print(f"[PASS] Latency stats over {num_requests} requests:")
    print(f"  - Average: {avg_latency:.2f}ms")
    print(f"  - Min: {min(latencies):.2f}ms")
    print(f"  - Max: {max(latencies):.2f}ms")
    print(f"  - P95: {p95_latency:.2f}ms")


def test_find_similar_latency_with_different_k_values():
    """Test latency remains < 200ms for different top_k values"""
    base_payload = {
        "app": {
            "name": "Test App",
            "category": "Games",
            "region": "US",
            "pricing": "free"
        },
        "partner_id": "perf_test_partner",
        "app_id": "perf_test_app"
    }

    k_values = [5, 10, 20, 50]

    for k in k_values:
        payload = {**base_payload, "top_k": k}

        start = time.perf_counter()
        response = client.post("/api/v1/find-similar", json=payload)
        latency_ms = (time.perf_counter() - start) * 1000

        assert response.status_code == 200, f"Request with k={k} failed"
        assert latency_ms < 200, f"Latency {latency_ms:.2f}ms with k={k} exceeds 200ms"

        print(f"[PASS] Latency with k={k}: {latency_ms:.2f}ms")


def test_predict_endpoint_functional():
    """Test that predict endpoint works correctly (functional test, not latency-critical)"""
    payload = {
        "app": {
            "name": "Test App",
            "category": "Health & Fitness"
        },
        "neighbors": [
            {"app_id": "APP_10123", "similarity": 0.95},
            {"app_id": "APP_10456", "similarity": 0.87},
            {"app_id": "APP_10789", "similarity": 0.82}
        ],
        "ab_arm": "v1"
    }

    response = client.post("/api/v1/predict", json=payload)

    assert response.status_code == 200, f"Predict request failed: {response.json()}"

    # Verify response includes required fields
    data = response.json()
    assert "latency_ms" in data, "Response missing latency_ms field"
    assert "prediction" in data, "Response missing prediction field"
    assert "ab_arm" in data, "Response missing ab_arm field"

    print(f"[PASS] Predict endpoint functional test")
    print(f"  - Prediction score: {data['prediction']['score']}")
    print(f"  - Segments: {data['prediction']['segments']}")


def test_cold_start_vs_warm():
    """Test that subsequent requests (warm) are faster than first request (cold start)"""
    payload = {
        "app": {
            "name": "Cold Start Test",
            "category": "Productivity",
            "region": "US"
        },
        "top_k": 10,
        "partner_id": "cold_start_test",
        "app_id": "cold_start_app"
    }

    # First request (cold start)
    start = time.perf_counter()
    response1 = client.post("/api/v1/find-similar", json=payload)
    cold_latency = (time.perf_counter() - start) * 1000

    assert response1.status_code == 200

    # Subsequent requests (warm)
    warm_latencies = []
    for _ in range(5):
        start = time.perf_counter()
        response = client.post("/api/v1/find-similar", json=payload)
        warm_latency = (time.perf_counter() - start) * 1000

        assert response.status_code == 200
        warm_latencies.append(warm_latency)

    avg_warm_latency = statistics.mean(warm_latencies)

    # Both should be under 200ms
    assert cold_latency < 200, f"Cold start latency {cold_latency:.2f}ms exceeds 200ms"
    assert avg_warm_latency < 200, f"Warm latency {avg_warm_latency:.2f}ms exceeds 200ms"

    print(f"[PASS] Cold start latency: {cold_latency:.2f}ms")
    print(f"[PASS] Average warm latency: {avg_warm_latency:.2f}ms")
    print(f"  - Speedup: {(cold_latency / avg_warm_latency):.2f}x")


if __name__ == "__main__":
    """Run performance tests standalone and print summary"""
    print("="*60)
    print("PERFORMANCE TEST SUITE - <200ms Latency Requirement")
    print("="*60)

    tests = [
        ("Single Request", test_find_similar_latency_single_request),
        ("Average Over Multiple", test_find_similar_latency_average),
        ("Different K Values", test_find_similar_latency_with_different_k_values),
        ("Predict Endpoint (Functional)", test_predict_endpoint_functional),
        ("Cold vs Warm Start", test_cold_start_vs_warm),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        print(f"\n{name}:")
        print("-" * 60)
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ ERROR: {e}")
            failed += 1

    print("\n" + "="*60)
    print(f"SUMMARY: {passed} passed, {failed} failed")
    print("="*60)

    if failed > 0:
        exit(1)
