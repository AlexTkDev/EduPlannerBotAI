import os
import pytest
from services.txt import save_plan_to_txt

@pytest.mark.asyncio
async def test_save_plan_to_txt(tmp_path):
    plan_lines = ["Step 1", "Step 2", "Step 3"]
    user_id = 12345
    # Override the working directory 'plans' to a temporary one
    plans_dir = tmp_path / "plans"
    plans_dir.mkdir()
    orig_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        filename = await save_plan_to_txt(plan_lines, user_id)
        assert os.path.exists(filename)
        with open(filename, encoding="utf-8") as f:
            content = f.read().splitlines()
        assert content == plan_lines
    finally:
        os.chdir(orig_cwd) 