from services import local_llm


class DummyModel:
    def __call__(self, *_args, **_kwargs):
        return {"choices": [{"text": "ok"}]}


def test_normalize_max_tokens():
    assert local_llm._normalize_max_tokens(-1) == local_llm.LOCAL_LLM_MAX_TOKENS
    assert local_llm._normalize_max_tokens("bad") == local_llm.LOCAL_LLM_MAX_TOKENS
    assert local_llm._normalize_max_tokens(1_000_000) == local_llm.LOCAL_LLM_CONTEXT


def test_ask_local_llm_empty_prompt(monkeypatch):
    monkeypatch.setattr(local_llm, "LLM_MODEL", DummyModel())
    result = local_llm.ask_local_llm("   ")
    assert result == "[Local LLM error: Empty prompt]"
