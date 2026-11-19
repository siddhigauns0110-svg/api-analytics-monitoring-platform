import requests
from monitor import check_endpoint

class FakeResponse:
    status_code = 200

def test_successful_endpoint(monkeypatch):
    monkeypatch.setattr(requests, "request", lambda **kwargs: FakeResponse())
    result = check_endpoint({"name": "demo", "url": "https://example.com"})
    assert result["is_success"] is True
    assert result["status_code"] == 200
    assert result["response_time_ms"] >= 0

def test_request_error(monkeypatch):
    def raise_error(**kwargs):
        raise requests.Timeout("timed out")
    monkeypatch.setattr(requests, "request", raise_error)
    result = check_endpoint({"name": "demo", "url": "https://example.com"})
    assert result["is_success"] is False
    assert result["status_code"] is None
    assert "Timeout" in result["error_message"]
