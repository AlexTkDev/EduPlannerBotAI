import importlib


def test_local_llm_int_env_fallbacks(monkeypatch):
    monkeypatch.setenv("LOCAL_LLM_CONTEXT", "invalid")
    monkeypatch.setenv("LOCAL_LLM_THREADS", "0")
    monkeypatch.setenv("LOCAL_LLM_MAX_TOKENS", "-10")

    import config
    importlib.reload(config)

    assert config.LOCAL_LLM_CONTEXT == 4096
    assert config.LOCAL_LLM_THREADS == 4
    assert config.LOCAL_LLM_MAX_TOKENS == 512


def test_local_llm_int_env_valid(monkeypatch):
    monkeypatch.setenv("LOCAL_LLM_CONTEXT", "8192")
    monkeypatch.setenv("LOCAL_LLM_THREADS", "8")
    monkeypatch.setenv("LOCAL_LLM_MAX_TOKENS", "1024")

    import config
    importlib.reload(config)

    assert config.LOCAL_LLM_CONTEXT == 8192
    assert config.LOCAL_LLM_THREADS == 8
    assert config.LOCAL_LLM_MAX_TOKENS == 1024
