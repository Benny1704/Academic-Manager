from models import User
from storage import load_json
from functools import wraps

def _load_user(filepath:str):
    data = load_json(filepath)
    return [User(**user) for user in data]

def login_required(session):
    def decorator(base_fn):
        @wraps(base_fn)
        def enhanced_fn(*args, **kwargs):
            users = _load_user("data/users.json")
            for user in users:
                if user.user_id == session.get("current_user") and user.is_logged_in:
                    return base_fn(*args, **kwargs)
            return {
                "status": False,
                "error": "Login Required!!"
            }
        return enhanced_fn
    return decorator
