import os
import logging
import aiofiles

logger = logging.getLogger(__name__)

async def save_plan_to_txt(plan_lines: list[str], user_id: int) -> str:
    """Save the study plan to a TXT file asynchronously."""
    os.makedirs("plans", exist_ok=True)
    filename = f"plans/plan_{user_id}.txt"
    try:
        async with aiofiles.open(filename, "w", encoding="utf-8") as f:
            for line in plan_lines:
                await f.write(line + "\n")
    except Exception as e:
        logger.error("Failed to write TXT file: %s", e)
        raise
    return filename
