import os
import tempfile
from services.pdf import save_plan_to_pdf

def test_save_plan_to_pdf(tmp_path):
    plan_lines = ["Step 1", "Step 2", "Step 3"]
    user_id = 54321
    # Override the working directories 'plans' and 'fonts' to temporary ones
    plans_dir = tmp_path / "plans"
    fonts_dir = tmp_path / "fonts"
    plans_dir.mkdir()
    fonts_dir.mkdir()
    orig_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        filename = save_plan_to_pdf(plan_lines, user_id)
        assert os.path.exists(filename)
        assert filename.endswith(f"plan_{user_id}.pdf")
    finally:
        os.chdir(orig_cwd) 