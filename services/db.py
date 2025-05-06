from tinydb import TinyDB

db = TinyDB("db.json")

def save_user_plan(user_id: int, plan: list):
    db.insert({"user_id": user_id, "plan": plan})
