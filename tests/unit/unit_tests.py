import pytest
import requests
from src.mesh import Mediator

def test_mediator_reintentos(monkeypatch):
    # Simula servicio A caído
    class FakeResp:
        def raise_for_status(self):
            raise requests.ConnectionError()
    monkeypatch.setattr(requests, "post", lambda *a, **kw: FakeResp())
    mediator = Mediator('http://x', 'http://y', 'http://z')
    with pytest.raises(Exception):
        mediator.execute({'trace_id': 't1', 'data': 'd'})

def test_mediator_b_lento(monkeypatch):
    # Simula servicio B lento
    class FakeResp:
        def __init__(self, elapsed):
            self._json = {"data": "ok", "trace_id": "t1"}
            self.elapsed = elapsed
        def raise_for_status(self):
            pass
        def json(self):
            return self._json
    monkeypatch.setattr(requests, "post", lambda *a, **kw: FakeResp(type('Elapsed', (), {'total_seconds': lambda self: 1})()))
    mediator = Mediator('http://x', 'http://y', 'http://z')
    res = mediator.execute({'trace_id': 't1', 'data': 'd'})
    assert "B lento" in res["data"]
