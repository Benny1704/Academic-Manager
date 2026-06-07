from models import User, UserRole, Student, Course
from validators import is_valid_username, is_valid_email, is_valid_phone, is_valid_password

class UserService:

  users = []

  def __init__(self,filepath:str):
    self.users = []
    self.filepath = filepath

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

    if errors:
      return {
        "status": False,
        "error": errors
      }

    user = User(username,email,phone,password,role)
    self.users.append(user)

    return {
            "success": True,
            "message": "User added successfully",
            "user": user
        }