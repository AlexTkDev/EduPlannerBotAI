import os
import tempfile
import pytest
from services.db import save_user_plan, get_user_plan
from tinydb import TinyDB

def test_save_and_get_user_plan(monkeypatch):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        db_path = tmp.name
    try:
        # Override the database path
        monkeypatch.setattr('services.db.db', TinyDB(db_path))
        user_id = 42
        plan = ["A", "B", "C"]
        save_user_plan(user_id, plan)
        loaded = get_user_plan(user_id)
        assert loaded == plan
    finally:
        os.remove(db_path) 