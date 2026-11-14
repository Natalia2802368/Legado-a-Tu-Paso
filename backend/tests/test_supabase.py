from pydantic import SecretStr

import app.core.supabase as supabase_module


def test_get_supabase_client_uses_configured_credentials(monkeypatch):
    expected_client = object()
    captured = {}

    monkeypatch.setattr(
        supabase_module.settings,
        "supabase_url",
        "https://example.supabase.co",
    )

    monkeypatch.setattr(
        supabase_module.settings,
        "supabase_secret_key",
        SecretStr("test-secret"),
    )

    def fake_create_client(url, key):
        captured["url"] = url
        captured["key"] = key
        return expected_client

    monkeypatch.setattr(
        supabase_module,
        "create_client",
        fake_create_client,
    )

    supabase_module.get_supabase_client.cache_clear()

    try:
        client = supabase_module.get_supabase_client()
    finally:
        supabase_module.get_supabase_client.cache_clear()

    assert client is expected_client
    assert captured["url"] == "https://example.supabase.co"
    assert captured["key"] == "test-secret"