from tinydb import TinyDB, Query

db = TinyDB("db.json")


def save_user_plan(user_id: int, plan: list):
    """Save user study plan to the database"""
    user_query = Query()
    db.upsert({"user_id": user_id, "plan": plan}, user_query.user_id == user_id)


def get_user_plan(user_id: int) -> list:
    """Get user study plan from the database"""
    user_query = Query()
    result = db.search(user_query.user_id == user_id)
    return result[0].get("plan", []) if result else []


def get_all_user_plans(user_id: int) -> list:
    """Get all user study plans from the database"""
    user_query = Query()
    return db.search(user_query.user_id == user_id)


def delete_user_plan(user_id: int) -> bool:
    """Delete user study plan from the database"""
    user_query = Query()
    return bool(db.remove(user_query.user_id == user_id))


def set_user_language(user_id: int, language: str):
    """Set user's preferred language in the database."""
    user_query = Query()
    db.upsert({"user_id": user_id, "language": language}, user_query.user_id == user_id)

def get_user_language(user_id: int) -> str:
    """Get user's preferred language from the database. Defaults to 'en'."""
    user_query = Query()
    result = db.search(user_query.user_id == user_id)
    if result and "language" in result[0]:
        return result[0]["language"]
    return "en"
