from dataclasses import asdict
from decorators import login_required
from models import User, UserRole, Student, Course
from storage import load_json, save_json
from validators import is_valid_role, is_valid_username, is_valid_email, is_valid_phone, is_valid_password, is_valid_name, is_valid_age, is_valid_mark

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
            "message": f"{user.username} added successfully",
            "user": user
        }
  
  def login_user(self,username,email,password) -> dict:

    users = self._load_users()
    for user in users:
      if (user.username == username or user.email == email) and user.password == password:
        user.is_logged_in = True
        self._save_users(users)
        return {
          "status": True,
          "message": f"Login Successfull, Welcome {user.username}",
          "current_user": user.user_id
        }
    return {
          "status": False,
          "error": f"Login Unsuccessfull, Invalid Credentials!",
          "current_user": None
        }
  
class StudentService:
  
  def __init__(self,filepath:str):
    self.filepath = filepath

  def _load_students(self) -> list[Student]:
    data = load_json(self.filepath)
    return [Student(**student) for student in data]
  
  def _save_students(self,students: list[Student]) -> None:
    data = [asdict(student) for student in students]
    save_json(self.filepath,data)

  def _get_grade(self, mark: int) -> str:
    if mark >= 90:
      return "A"
    if mark >= 80:
      return "B"
    if mark >= 70:
      return "C"
    if mark >= 60:
      return "D"
    return "F"

  def _get_status(self, mark: int) -> str:
    return "Pass" if mark >= 35 else "Fail"

  def add_student(self,name,age,email,phone,mark) -> dict:
    errors = []
    if not is_valid_name(name):
      errors.append(f"Invalid name: {name}")
      
    if not is_valid_age(age):
      errors.append(f"Invalid age: {age}")
      
    if not is_valid_email(email):
      errors.append(f"Invalid email: {email}")
      
    if not is_valid_phone(phone):
      errors.append(f"Invalid phone: {phone}")
      
    if not is_valid_mark(mark):
      errors.append(f"Invalid mark: {mark}")

    if errors:
      return {
        "status": False,
        "error": errors
      }
    
    students = self._load_students()
    next_id = 1

    if students:
      for student in students:
        if student.email == email:
          return {
            "status": False,
            "error": f"email already exists: {email}"
          }
      next_id = max(student.student_id for student in students) + 1
    
    student = Student(student_id=next_id,name=name,age=age,email=email,phone=phone,mark=mark)
    students.append(student)
    self._save_students(students)

    return {
      "status": True,
      "message": f"{student.name} has been added successfully"
    }
  
  def view_students(self) -> None:
    students = self._load_students()

    if not students:
        print("No students found")
        return

    for index, student in enumerate(students):
        courses = ", ".join(student.enrolled_courses) if student.enrolled_courses else "None"
        print()
        print(f"---------> Student {index + 1} <---------")
        print(f"ID: {student.student_id}")
        print(f"Name: {student.name}")
        print(f"Age: {student.age}")
        print(f"Email: {student.email}")
        print(f"Phone: {student.phone}")
        print(f"Mark: {student.mark}")
        print(f"Grade: {self._get_grade(student.mark)}")
        print(f"Status: {self._get_status(student.mark)}")
        print(f"Courses: {courses}")
        print()

  def search_student(self,name,email,phone) -> None:
    students = self._load_students()

    if not students:
        print("No students found")
        return

    for student in students:
      if student.name == name or student.email == email or student.phone == phone:
        student_found = True
        courses = ", ".join(student.enrolled_courses) if student.enrolled_courses else "None"
        print()
        print(f"---------> Student Details <---------")
        print(f"ID: {student.student_id}")
        print(f"Name: {student.name}")
        print(f"Age: {student.age}")
        print(f"Email: {student.email}")
        print(f"Phone: {student.phone}")
        print(f"Mark: {student.mark}")
        print(f"Grade: {self._get_grade(student.mark)}")
        print(f"Status: {self._get_status(student.mark)}")
        print(f"Courses: {courses}")
        print()
        return

    print("Cant find student for your search")
        

    
  
