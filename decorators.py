from models import User, UserRole
from storage import load_json
from functools import wraps

def _load_user(filepath:str):
    data = load_json(filepath)
    users = []
    for user in data:
        role = user.get("role")
        if isinstance(role, str):
            try:
                user["role"] = UserRole(role)
            except ValueError:
                pass
        users.append(User(**user))
    return users

def login_required(session):
    def decorator(base_fn):
        @wraps(base_fn)
        def enhanced_fn(*args, **kwargs):
            users = _load_user("data/users.json")
            for user in users:
                if user.user_id == session.get("user_id") and user.is_logged_in:
                    return base_fn(*args, **kwargs)
            return {
                "status": False,
                "error": "Login Required!!"
            }
        return enhanced_fn
    return decorator

def admin_required(session):
    def decorator(base_fn):
        @wraps(base_fn)
        def enhanced_fn(*args, **kwargs):
            users = _load_user("data/users.json")
            for user in users:
                if user.user_id == session.get("user_id") and user.role == UserRole.ADMIN:
                    return base_fn(*args, **kwargs)
            return {
                "status": False,
                "error": "Admin Role Required!!"
            }
        return enhanced_fn
    return decorator
