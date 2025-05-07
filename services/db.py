from tinydb import TinyDB, Query

db = TinyDB("db.json")


def save_user_plan(user_id: int, plan: list):
    """Сохранить учебный план пользователя в базу данных"""
    User = Query()
    db.upsert({"user_id": user_id, "plan": plan}, User.user_id == user_id)


def get_user_plan(user_id: int) -> list:
    """Получить учебный план пользователя из базы данных"""
    User = Query()
    result = db.search(User.user_id == user_id)
    return result[0].get("plan", []) if result else []


def get_all_user_plans(user_id: int) -> list:
    """Получить все планы конкретного пользователя"""
    User = Query()
    return db.search(User.user_id == user_id)


def delete_user_plan(user_id: int) -> bool:
    """Удалить учебный план пользователя из базы данных"""
    User = Query()
    return bool(db.remove(User.user_id == user_id))
