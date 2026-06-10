from dataclasses import asdict
from models import CardPayment, CashPayment, Course, Payment, PaymentMethod, UPIPayment, User, UserRole, Student
from storage import load_json, save_json
from validators import is_valid_fee, is_valid_role, is_valid_username, is_valid_email, is_valid_phone, is_valid_password, is_valid_name, is_valid_age, is_valid_mark, is_valid_week

class UserService:

  def __init__(self,filepath:str):
    self.filepath = filepath

  def _load_users(self) -> list[User]:
    data = load_json(self.filepath)
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
  
  def _save_users(self,users: list[User]) -> None:
    data = [asdict(user) for user in users]
    save_json(self.filepath,data)

  def register_user(self,username,email,phone,password,role) -> dict:
    errors = []
    if not is_valid_username(username):
      errors.append(f"Invalid username: {username}")
      
    if not is_valid_email(email):
      errors.append(f"Invalid email: {email}")
      
    if not is_valid_phone(phone):
      errors.append(f"Invalid phone: {phone}")
      
    if not is_valid_password(password):
      errors.append(f"Invalid password: {password}")
    
    role_enum = is_valid_role(role)
    if role_enum is None:
      errors.append(f"Invalid role: {role}. Allowed roles: admin, staff, student")

    if errors:
      return {
        "status": False,
        "error": errors
      }
    
    users = self._load_users()

    next_id = 1
    if users:
      max_id = 1
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
        if user.user_id > max_id:
          max_id = user.user_id
      next_id = max_id + 1

    user = User(next_id,username,email,phone,password,role_enum)
    users.append(user)
    self._save_users(users)

    return {
            "status": True,
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
          "user_id": user.user_id
        }
    return {
          "status": False,
          "error": f"Login Unsuccessfull, Invalid Credentials!",
          "user_id": None
        }
  
class StudentService:
  
  def __init__(self,filepath:str):
    self.filepath = filepath

  def _load_students(self) -> list[Student]:
    data = load_json(self.filepath)
    students = []
    for student in data:
      enrolled_courses = student.get("enrolled_courses", [])
      student["enrolled_courses"] = [Course(**course) if isinstance(course, dict) else course for course in enrolled_courses]
      students.append(Student(**student))
    return students
  
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
      max_id = 1
      for student in students:
        if student.email == email:
          return {
            "status": False,
            "error": f"email already exists: {email}"
          }
        if student.student_id > max_id:
          max_id = student.student_id
      next_id = max_id + 1
    
    student = Student(student_id=next_id,name=name,age=age,email=email,phone=phone,mark=mark,grade=self._get_grade(mark),status=self._get_status(mark))
    students.append(student)
    self._save_students(students)

    return {
      "status": True,
      "message": f"{student.name} has been added successfully"
    }
  
  def view_students(self) -> dict:
    students = self._load_students()

    if not students:
      return {
        "status": False,
        "error": "No Students Found"
      }
    
    return {
      "status": True,
      "students": students
    }

  def search_students(self,name,email,phone) -> dict:
    students = self._load_students()
    found_students = []

    if not students:
      return {
        "status": False,
        "error": "No Students Found"
      }

    for student in students:
      if student.name == name or student.email == email or student.phone == phone:
        found_students.append(student)

    if found_students:
      return {
          "status": True,
          "students": found_students
        }

    return {
      "status": False,
      "error": "Cant find student for your search"
    }

  def update_student_mark(self,student_id,new_mark):

    if not is_valid_mark(new_mark):
      return {
        "status": False,
        "error": "Invalid Mark"
      }

    students = self._load_students()

    if not students:
      return {
        "status": False,
        "error": "No Students Found"
      }
    
    for student in students:
      if student.student_id == student_id:
        student.mark = new_mark
        student.grade=self._get_grade(student.mark)
        student.status=self._get_status(student.mark)
        self._save_students(students)
        return {
          "status": True,
          "message": f"Updated {student.name}'s mark to {student.mark}"
        }
    return {
      "status": False,
      "error": f"Student ID {student_id} not found"
    }

  def delete_student(self,student_id):
    students = self._load_students()

    if not students:
      return {
        "status": False,
        "error": "No Students Found"
      }

    new_students = [s for s in students if s.student_id != student_id]
    if len(new_students) == len(students):
      return {
        "status": False,
        "error": f"Student ID {student_id} not found"
      }

    self._save_students(new_students)
    return {
      "status": True,
      "message": f"Successfully deleted Student ID: {student_id}"
    }
  
  def get_student_by_id(self, student_id: int):
    """Get a single student by ID. Returns Student object or None."""
    students = self._load_students()
    for student in students:
      if student.student_id == student_id:
        return student
    return None

class CourseService:

  def __init__(self,filepath:str):
    self.filepath = filepath

  def _load_courses(self) -> list[Course]:
    data = load_json(self.filepath)
    return [Course(**course) for course in data]

  def _save_courses(self,courses: list[Course]) -> None:
    data = [asdict(course) for course in courses]
    save_json(self.filepath,data)

  def add_course(self,name,fee,duration_weeks):
    errors = []

    if not is_valid_name(name):
      errors.append(f"Invalid Course Name: {name}")
      
    if not is_valid_fee(fee):
      errors.append(f"Invalid Course Fee: {fee}")
      
    if not is_valid_week(duration_weeks):
      errors.append(f"Invalid Course Duration(In Weeks): {duration_weeks}")

    if errors:
      return {
        "status": False,
        "error": errors
      }
    
    courses = self._load_courses()

    next_id = 1

    if courses:
      max_id = 0
      for course in courses:
          if course.name.lower() == name.lower():
              return { "status": False, "error": "Course name already exists" }
          
          if course.course_id > max_id:
              max_id = course.course_id
              
      next_id = max_id + 1

    course = Course(course_id=next_id,name=name,fee=fee,duration_weeks=duration_weeks)
    courses.append(course)
    self._save_courses(courses)

    return {
      "status": True,
      "message": f"Successfully added Course: {name}",
      "courses": courses
    }

class EnrollmentService:

  def __init__(self, student_filepath: str, course_filepath: str):
    self.student_service = StudentService(student_filepath)
    self.course_service = CourseService(course_filepath)

  def enroll_student(self, student_id: int, course_id: int) -> dict:
    students = self.student_service._load_students()
    courses = self.course_service._load_courses()

    if not students:
      return {
        "status": False,
        "error": "No Students Found"
      }
    
    if not courses:
      return {
        "status": False,
        "error": "No Courses Found"
      }

    target_course = None
    for course in courses:
      if course.course_id == course_id:
        target_course = course
        break
    
    if not target_course:
      return {"status": False, "error": f"Course ID {course_id} not found."}
    
    student_found = False
    for student in students:
      if student.student_id == student_id:
          student_found = True
          
          if any(course.course_id == course_id for course in student.enrolled_courses):
            return {"status": False, "error": f"Student is already enrolled in this course."}
          student.enrolled_courses.append(target_course)
          break

    if not student_found:
      return {"status": False, "error": f"Student ID {student_id} not found."}
    
    self.student_service._save_students(students)

    return {
      "status": True, 
      "message": f"Successfully enrolled student {student_id} into course '{target_course.name}'"
    }
    
class PaymentService:

  def __init__(self,filepath:str):
    self.filepath = filepath

    self.__methods = {
      PaymentMethod.CASH: CashPayment(),
      PaymentMethod.UPI: UPIPayment(),
      PaymentMethod.CARD: CardPayment(),
    }

  def _load_payments(self) -> list[Payment]:
    data = load_json(self.filepath)
    payments = []
    for payment in data:
      method = payment.get("payment_method")
      if isinstance(method, str):
        try:
          payment["payment_method"] = PaymentMethod(method)
        except ValueError:
          pass
      payments.append(Payment(**payment))
    return payments

  def _save_payments(self,payments: list[Payment]) -> None:
    data = [asdict(payment) for payment in payments]
    save_json(self.filepath,data)

  def make_fee_payment(self,student_id,course_id,amount,payment_method: str):

    try:
      payment_method = PaymentMethod(payment_method.strip().lower())
    except ValueError:
      return {"status": False, "error": "Invalid payment method. Use cash, upi, or card"}

    payment = self.__methods[payment_method]
    method,message = payment.pay(amount)

    payments = self._load_payments()

    next_id = 1
    if payments:
      next_id = max(payment.payment_id for payment in payments) + 1

    payment_record = Payment(payment_id=next_id,student_id=student_id,course_id=course_id,amount=amount,payment_method=payment_method,message=message)
    payments.append(payment_record)
    self._save_payments(payments)

    return {"status": True, "record": payment_record}

  def get_student_payments(self, student_id: int) -> list[Payment]:
    """Get all payments for a specific student."""
    payments = self._load_payments()
    return [p for p in payments if p.student_id == student_id]
