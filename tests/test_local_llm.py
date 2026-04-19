from services import local_llm


class DummyModel:
    """Simple callable model stub for local LLM tests."""

    def __init__(self):
        self.last_kwargs = {}

    def __call__(self, *_args, **kwargs):
        self.last_kwargs = kwargs
        return {"choices": [{"text": "ok"}]}


def test_ask_local_llm_empty_prompt(monkeypatch):
    dummy_model = DummyModel()
    monkeypatch.setattr(local_llm, "LLM_MODEL", dummy_model)
    result = local_llm.ask_local_llm("   ")
    assert result == "[Local LLM error: Empty prompt]"


def test_ask_local_llm_normalizes_max_tokens(monkeypatch):
    dummy_model = DummyModel()
    monkeypatch.setattr(local_llm, "LLM_MODEL", dummy_model)

    result = local_llm.ask_local_llm("build plan", max_tokens=-1)

    assert result == "ok"
    assert dummy_model.last_kwargs["max_tokens"] == local_llm.LOCAL_LLM_MAX_TOKENS