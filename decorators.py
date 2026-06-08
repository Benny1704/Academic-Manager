from models import User
from storage import load_json
from functools import wraps

def _load_user(filepath:str):
    data = load_json(filepath)
    return [User(**user) for user in data]

def login_required(base_fn):
    @wraps(base_fn)
    def enhanced_fn(current_user):
        users = _load_user("data/users.json")
        for user in users:
            if user.user_id == current_user and user.is_logged_in == True:
                return base_fn(current_user)
        return {
            "status": False,
            "error": "Login required"
        }
    return enhanced_fn