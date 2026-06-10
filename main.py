from decorators import admin_required, login_required
from models import Student
from services import CourseService, EnrollmentService, PaymentService, UserService, StudentService
from reports import DashboardService, ReportService

session = {"user_id": None}
userService = UserService("data/users.json")
studentService = StudentService("data/students.json")
courseService = CourseService("data/courses.json")
enrollmentService = EnrollmentService(studentService, courseService)
paymentService = PaymentService("data/payments.json")
reportService = ReportService(studentService, paymentService)
dashboardService = DashboardService(userService, studentService, courseService, paymentService)

print("Welcome to Academic Manager!")
print("----------------------------")
is_new_user = input("New User? Y/N: ")

def register_user() -> dict:
    print()
    print("---------> Register User <---------")
    username = input("Enter Username: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")
    password = input("Enter Password: ")
    role = input("Enter Role: ")

    return userService.register_user(username=username, email=email, phone=phone, password=password, role=role)

def login_user():
    print("\n")
    print("---------> Login User <---------")
    username = input("Enter Username: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")

    return userService.login_user(username=username, email=email, password=password)

def read_int(prompt: str) -> int:
    """Read and validate integer input from user."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print()
            print("Please enter a valid number.")

def print_action_error(result):
    if isinstance(result, dict) and result.get("status") is False:
        print()
        print(result["error"])

@login_required(session)
def add_student():
    print()
    print("---------> Add Student <---------")
    name = input("Enter Name: ")
    age = read_int("Enter Age: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")
    mark = read_int("Enter Mark: ")
    student_add_result = studentService.add_student(name=name, age=age, email=email, phone=phone, mark=mark)
    if student_add_result["status"]:
        print()
        print(student_add_result["message"])
    else:
        print()
        print(student_add_result["error"])

@login_required(session)
def view_students():
    print()
    print("---------> View Students <---------")
    view_students_result = studentService.view_students()
    
    if view_students_result["status"]:
        students = view_students_result["students"]
        for index, student in enumerate(students):
            courses = ", ".join(course.name for course in student.enrolled_courses) if student.enrolled_courses else "None"
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
        print()
        print(view_students_result["error"])

@login_required(session)
def search_student():
    print("---------> Search Student <---------")
    name = input("Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    search_student_result = studentService.search_students(name=name, email=email, phone=phone)

    if search_student_result["status"]:
        students = search_student_result["students"]
        print()
        print(f"---------> Students Found ({len(students)}) <---------")
        for index, student in enumerate(students):
            courses = ", ".join(course.name for course in student.enrolled_courses) if student.enrolled_courses else "None"
            print()
            print(f"---------> Student {index} Details <---------")
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
        print()
        print(search_student_result["error"])

@login_required(session)
def update_student_mark():
    print("---------> Update Student Mark <---------")
    student_id = read_int("Enter Student ID: ")
    mark = read_int("Enter New Mark: ")
    update_student_mark_result = studentService.update_student_mark(student_id=student_id, new_mark=mark)

    if update_student_mark_result["status"]:
        print()
        print(update_student_mark_result["message"])
    else:
        print()
        print(update_student_mark_result["error"])

@login_required(session)
@admin_required(session)
def delete_student():
    print("---------> Delete Student <---------")
    student_id = read_int("Enter Student ID: ")
    delete_student_result = studentService.delete_student(student_id=student_id)

    if delete_student_result["status"]:
        print()
        print(delete_student_result["message"])
    else:
        print()
        print(delete_student_result["error"])

@login_required(session)
@admin_required(session)
def add_course():
    print("---------> Add Course <---------")
    name = input("Enter Course Name: ")
    fee = read_int("Enter Course Fee: ")
    duration_weeks = read_int("Enter Course Duration(In weeks): ")
    
    course_add_result = courseService.add_course(name=name, fee=fee, duration_weeks=duration_weeks)
    if course_add_result["status"]:
        print()
        print(course_add_result["message"])
    else:
        print()
        print(course_add_result["error"])

@login_required(session)
@admin_required(session)
def enroll_course():
    print("---------> Enroll Course <---------")
    student_id = read_int("Enter Student ID: ")
    course_id = read_int("Enter Course ID: ")
    
    enroll_course_result = enrollmentService.enroll_student(student_id=student_id, course_id=course_id)
    if enroll_course_result["status"]:
        print()
        print(enroll_course_result["message"])
    else:
        print()
        print(enroll_course_result["error"])

@login_required(session)
@admin_required(session)
def fee_payment():
    print("---------> Fee Payment <---------")
    student_id = read_int("Enter Student ID: ")
    course_id = read_int("Enter Course ID: ")
    amount = read_int("Enter Payment Fee : ₹")
    payment_method = input("Enter Payment Method: ")
    
    payment_result = paymentService.make_fee_payment(student_id=student_id, course_id=course_id, amount=amount, payment_method=payment_method)
    if payment_result["status"]:
        record = payment_result["record"]
        print()
        print(record.message)
    else:
        print()
        print(payment_result["error"])

@login_required(session)
@admin_required(session)
def student_report():
    print("---------> View Student Report <---------")
    student_id = read_int("Enter Student ID: ")

    result = reportService.student_report(student_id)

    if result["status"]:
        student = result["student"]
        payments = result["payments"]
        total_fees_paid = result["total_fees_paid"]
        
        courses = ", ".join(course.name for course in student.enrolled_courses) if student.enrolled_courses else "None"
        print()
        print("---------> Student Report <---------")
        print(f"ID: {student.student_id}")
        print(f"Name: {student.name}")
        print(f"Age: {student.age}")
        print(f"Email: {student.email}")
        print(f"Phone: {student.phone}")
        print(f"Mark: {student.mark}")
        print(f"Grade: {student.grade}")
        print(f"Status: {student.status}")
        print(f"Courses: {courses}")
        print(f"Total Fees Paid: ₹{total_fees_paid}")
        
        if payments:
            print("\nPayment History:")
            for payment in payments:
                print(f"  - Course ID {payment.course_id}: ₹{payment.amount} via {payment.payment_method.value}")
        else:
            print("\nPayment History: No payments made")
        print()
    else:
        print()
        print(result["error"])




    
    

def menu():
    while True:
        print("\n")
        print("---------> Menu <---------")
        print()
        print("1. Add Students")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student Mark")
        print("5. Delete Student")
        print("6. Add Course")
        print("7. Enroll Student in Course")
        print("8. Make Fee Payment")
        print("9. Student Report")
        print("10. Summary Dashboard ")
        print()

        option = read_int("Enter what you wanna do? : ")

        match option:
            case 1:
                print_action_error(add_student())
            case 2:
                print_action_error(view_students())
            case 3:
                print_action_error(search_student())
            case 4:
                print_action_error(update_student_mark())
            case 5:
                print_action_error(delete_student())
            case 6:
                print_action_error(add_course())
            case 7:
                print_action_error(enroll_course())
            case 8:
                print_action_error(fee_payment())
            case 9:
                print_action_error(student_report())
            case 10:
                dashboardService.summary_dashboard()
            case _:
                print("Invalid option")
                continue
        
        print()
        is_menu = input("Do you want to go back to menu? (Y/N): ")
        if is_menu.lower() != 'y':
            logout()
            break

def logout():
    session["user_id"] = None

if is_new_user.lower() == 'y':
    user_register_result = register_user()
    if user_register_result["status"]:
        print(user_register_result["message"])
    else:
        print(user_register_result["error"])

user_login_result = login_user()
if user_login_result["status"]:
    print(user_login_result["message"])
    session["user_id"] = user_login_result["user_id"]
    menu()
else:
    print(user_login_result["error"])
