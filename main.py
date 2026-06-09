from decorators import login_required
from services import UserService, StudentService

session = {"current_user": None}
userService = UserService("data/users.json")
studentService = StudentService("data/students.json")

print("Welcome to Academic Manager!")
print("----------------------------")
is_new_user = input("New User? Y/N: ")

def register_user() -> dict:
    print("\n")
    print("---------> Register User <---------")
    username = input("Enter Username: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")
    password = input("Enter Password: ")
    role = input("Enter Role: ")

    return userService.register_user(username = username, email = email, phone = phone, password = password, role = role)

def login_user():
    print("\n")
    print("---------> Login User <---------")
    username = input("Enter Username: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")

    return userService.login_user(username = username ,email = email, password = password)

def read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def print_action_error(result):
    if isinstance(result, dict) and result.get("status") is False:
        print(result["error"])

@login_required(session)
def add_student():
    print("\n")
    print("---------> Add Student <---------")
    name = input("Enter Name: ")
    age = read_int("Enter Age: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")
    mark = read_int("Enter Mark: ")
    student_add_result = studentService.add_student(name = name, age = age, email = email, phone = phone, mark = mark)
    if(student_add_result["status"] == True):
        print(student_add_result["message"])
    else:
        print(student_add_result["error"])

@login_required(session)
def view_students():
    view_students_result = studentService.view_students()
    
    if(view_students_result["status"] == True):
        students = view_students_result["students"]
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
            print(f"Grade: {student.grade}")
            print(f"Status: {student.status}")
            print(f"Courses: {courses}")
            print()
    else:
        print(view_students_result["error"])

@login_required(session)
def search_student():
    name = input("Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    search_student_result = studentService.search_student(name=name,email=email,phone=phone)

    if(search_student_result["status"] == True):
        student = search_student_result["student"]
        courses = ", ".join(student.enrolled_courses) if student.enrolled_courses else "None"
        print()
        print(f"---------> Student Details <---------")
        print(f"ID: {student.student_id}")
        print(f"Name: {student.name}")
        print(f"Age: {student.age}")
        print(f"Email: {student.email}")
        print(f"Phone: {student.phone}")
        print(f"Mark: {student.mark}")
        print(f"Grade: {student.grade}")
        print(f"Status: {student.status}")
        print(f"Courses: {courses}")
        print()
        
    else:
        print(search_student_result["error"])

@login_required(session)
def update_student_mark():
    id = read_int("Enter Student ID: ")
    mark = read_int("Enter New Mark: ")
    update_student_mark_result = studentService.update_student_mark(student_id=id,new_mark=mark)

    if(update_student_mark_result["status"] == True):
        print(update_student_mark_result["message"])
    else:
        print(update_student_mark_result["error"])

def menu():
    print("\n")
    print("---------> Menu <---------")
    print()
    print("1. Add Students")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student Mark")

    option = read_int("Enter what you wanna do? : ")

    match(option):
        case 1:
            print_action_error(add_student())
        case 2:
            print_action_error(view_students())
        case 3:
            print_action_error(search_student())
        case 4:
            print_action_error(update_student_mark())
        case _:
            print("Invalid option")

if(is_new_user.lower() == 'y'):
    user_register_result = register_user()
    if(user_register_result["status"] == True):
        print(user_register_result["message"])
    else:
        print(user_register_result["error"])

user_login_result = login_user()
if(user_login_result["status"] == True):
    print(user_login_result["message"])
    session["current_user"] = user_login_result["current_user"]
    menu()
else:
    print(user_login_result["error"])
    session["current_user"] = user_login_result["current_user"]
