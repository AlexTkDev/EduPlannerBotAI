import pytest
from services.llm import generate_local_plan, generate_study_plan

@pytest.mark.parametrize("topic", ["Python", "Math", "History"])
def test_generate_local_plan(topic):
    plan = generate_local_plan(topic)
    assert isinstance(plan, list)
    assert any(topic in step for step in plan)
    assert len(plan) >= 5

@pytest.mark.asyncio
async def test_generate_study_plan_local(monkeypatch):
    # Disable OPENAI_API_KEY to check fallback to local generator
    monkeypatch.setattr("services.llm.OPENAI_API_KEY", None)
    plan = await generate_study_plan("TestTopic")
    assert isinstance(plan, list)
    assert any("TestTopic" in step for step in plan) 