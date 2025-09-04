import pytest
from services.llm import translate_text


@pytest.mark.asyncio
async def test_translate_english_passthrough(monkeypatch):
    # Ensure no online calls are attempted
    monkeypatch.setattr("services.llm.OPENAI_API_KEY", None)
    monkeypatch.setattr("services.llm.GROQ_API_KEY", None)
    text = "Hello world"
    result = await translate_text(text, "en")
    assert result == text


@pytest.mark.asyncio
async def test_translate_empty_text_passthrough(monkeypatch):
    monkeypatch.setattr("services.llm.OPENAI_API_KEY", None)
    monkeypatch.setattr("services.llm.GROQ_API_KEY", None)
    text = "   "
    result = await translate_text(text, "ru")
    assert result == text


@pytest.mark.asyncio
async def test_translate_local_fallback_success(monkeypatch):
    # Disable online providers to force local fallback
    monkeypatch.setattr("services.llm.OPENAI_API_KEY", None)
    monkeypatch.setattr("services.llm.GROQ_API_KEY", None)

    def fake_local_llm(_prompt: str, _max_tokens: int = 512) -> str:
        return "Привет мир"

    monkeypatch.setattr("services.llm.ask_local_llm", fake_local_llm)

    result = await translate_text("Hello world", "ru")
    assert result == "Привет мир"


@pytest.mark.asyncio
async def test_translate_all_failures_return_original(monkeypatch):
    # Disable online providers
    monkeypatch.setattr("services.llm.OPENAI_API_KEY", None)
    monkeypatch.setattr("services.llm.GROQ_API_KEY", None)

    def failing_local_llm(_prompt: str, _max_tokens: int = 512) -> str:
        return "[Local LLM error: test]"

    monkeypatch.setattr("services.llm.ask_local_llm", failing_local_llm)

    text = "Hello world"
    result = await translate_text(text, "ru")
    assert result == text


@pytest.mark.asyncio
async def test_translate_locale_normalization(monkeypatch):
    # Disable online providers to hit local fallback and ensure lang normalization (ru-RU -> ru)
    monkeypatch.setattr("services.llm.OPENAI_API_KEY", None)
    monkeypatch.setattr("services.llm.GROQ_API_KEY", None)

    def fake_local_llm(prompt: str, _max_tokens: int = 512) -> str:
        # Ensure that the prompt contains normalized 'ru' rather than 'ru-RU'
        assert "to ru." in prompt or "to ru]" in prompt or "to ru\n" in prompt
        return "Привет"

    monkeypatch.setattr("services.llm.ask_local_llm", fake_local_llm)

    result = await translate_text("Hi", "ru-RU")
    assert result == "Привет"
