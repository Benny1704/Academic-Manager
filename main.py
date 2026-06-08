from decorators import login_required
from services import UserService, StudentService

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

    userService = UserService("data/users.json")
    return userService.register_user(username = username, email = email, phone = phone, password = password, role = role)

def login_user():
    print("\n")
    print("---------> Login User <---------")
    username = input("Enter Username: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")

    userService = UserService("data/users.json")
    return userService.login_user(username = username ,email = email, password = password)

@login_required
def add_student(current_user):
    print("\n")
    print("---------> Add Student <---------")
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")
    mark = int(input("Enter Mark: "))

    studentService = StudentService("data/students.json")
    return studentService.add_student(current_user = current_user,name = name, age = age, email = email, phone = phone, mark = mark)

current_user = None
if(is_new_user.lower() == 'y'):
    user_register_result = register_user()
    if(user_register_result["status"] == True):
        print(user_register_result["message"])
    else:
        print(user_register_result["error"])

user_login_result = login_user()
if(user_login_result["status"] == True):
    print(user_login_result["message"])
    current_user = user_login_result["current_user"]
else:
    print(user_login_result["error"])
    current_user = user_login_result["current_user"]


print("\n")
print("---------> Menu <---------")
print("n")
print("1. Add Students")

option = int(input("Enter what you wanna do? : "))

match(option):
    case 1:
        student_add_result = add_student(current_user)
        if(student_add_result["status"] == True):
            print(student_add_result["message"])
        else:
            print(student_add_result["error"])