import re
from models import PaymentMethod, UserRole

def is_valid_username(username: str) -> bool:
  return bool(re.fullmatch(r"\w{3,15}",username))

def is_valid_email(email: str) -> bool:
  return bool(re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",email))

def is_valid_phone(phone: str) -> bool:
  return bool(re.fullmatch(r"\d{10}",phone))

def is_valid_password(password: str) -> bool:
  return bool(re.fullmatch(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",password))

def is_valid_name(name: str) -> bool:
  return bool(re.fullmatch(r"[a-zA-Z\s]+", name.strip()))

def is_valid_mark(mark: int) -> bool:
  return 0 <= mark <= 100

def is_valid_age(age: int) -> bool:
  return 1 <= age <= 120

def is_valid_week(week: int) -> bool:
  return 0 <= week <= 52

def is_valid_fee(age: int) -> bool:
  return 500 <= age <= 100000

def is_valid_role(role: str) -> UserRole | None:
  role = role.strip().lower()
  try:
    return UserRole(role)
  except ValueError:
    return None