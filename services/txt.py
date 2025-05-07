import os


def save_plan_to_txt(plan_lines: list[str], user_id: int) -> str:
    os.makedirs("plans", exist_ok=True)
    filename = f"plans/plan_{user_id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for line in plan_lines:
            f.write(line + "\n")
    return filename
