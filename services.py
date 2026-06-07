from dataclasses import asdict
from models import User, UserRole, Student, Course
from storage import load_json, save_json
from validators import is_valid_role, is_valid_username, is_valid_email, is_valid_phone, is_valid_password

class UserService:

  def __init__(self,filepath:str):
    self.filepath = filepath

  def _load_users(self) -> list[User]:
    data = load_json(self.filepath)
    return [User(**user) for user in data]

  def _save_users(self,users: list[User]) -> None:
    data = [asdict(user) for user in users]
    save_json(self.filepath,data)

  def register_user(self,username,email,phone,password,role: UserRole) -> dict:
    errors = []
    if not is_valid_username(username):
      errors.append(f"Invalid username: {username}")
      
    if not is_valid_email(email):
      errors.append(f"Invalid email: {email}")
      
    if not is_valid_phone(phone):
      errors.append(f"Invalid phone: {phone}")
      
    if not is_valid_password(password):
      errors.append(f"Invalid password: {password}")
    
    if is_valid_role(role) is None:
      errors.append(f"Invalid role: {role}. Allowed roles: admin, staff, student")

    if errors:
      return {
        "status": False,
        "error": errors
      }
    
    users = self._load_users()

    next_id = 1
    if users:
      for user in users:
        if user.email == email:
          return {
            "status": False,
            "error": f"email already exists: {email}"
          }
        if user.username == username:
          return {
            "status": False,
            "error": f"username already exists: {username}"
          }
      next_id = max(user.user_id for user in users) + 1

    user = User(next_id,username,email,phone,password,role)
    users.append(user)
    self._save_users(users)

    return {
            "success": True,
            "message": "User added successfully",
            "user": user
        }