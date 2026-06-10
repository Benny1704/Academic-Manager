from textwrap import dedent
from collections import Counter

from models import Student, Payment
from services import CourseService, StudentService, PaymentService, UserService

class ReportService:
    """Generates comprehensive reports by aggregating data from multiple services"""
    
    def __init__(self, student_service: StudentService, payment_service: PaymentService):
        self.student_service = student_service
        self.payment_service = payment_service

    def student_report(self, student_id: int) -> dict:
        """Generate comprehensive student report with academic and payment details"""
        # Get student
        student = self.student_service.get_student_by_id(student_id)
        if student is None:
            return {
                "status": False,
                "error": f"Student ID {student_id} not found"
            }
        
        # Get payments for this student
        payments = self.payment_service.get_student_payments(student_id)
        
        # Calculate total fees paid
        total_fees_paid = sum(p.amount for p in payments)
        
        return {
            "status": True,
            "student": student,
            "payments": payments,
            "total_fees_paid": total_fees_paid
        }

class DashboardService:
    """Generate comprehensive dashboard with analytics and statistics."""
    
    def __init__(self, user_service: UserService, student_service: StudentService, course_service: CourseService, payment_service: PaymentService):
        self.user_service = user_service
        self.student_service = student_service
        self.course_service = course_service
        self.payment_service = payment_service

    def summary_dashboard(self) -> dict:
        """Generate dashboard summary with statistics and return as dict."""
        users = self.user_service._load_users()
        students = self.student_service._load_students()
        courses = self.course_service._load_courses()
        payments = self.payment_service._load_payments()

        total_users = len(users)
        total_students = len(students)
        total_courses = len(courses)
        total_payments = len(payments)
        total_revenue = sum(payment.amount for payment in payments) if payments else 0

        def passed_students():
            """Yield students who passed."""
            for student in students:
                if student.status == "Pass":
                    yield student

        def failed_students():
            """Yield students who failed."""
            for student in students:
                if student.status == "Fail":
                    yield student
        
        # Calculate average mark with zero-division protection
        average_mark = (sum(student.mark for student in students) // total_students) if total_students > 0 else 0

        # Find topper (highest mark)
        max_mark = 0
        topper = None
        for student in students:
            if student.mark > max_mark:
                max_mark = student.mark
                topper = student
        
        # Find most expensive course
        max_cost = 0
        expensive_course = None
        for course in courses:
            if course.fee > max_cost:
                max_cost = course.fee
                expensive_course = course

        # Sort students by marks (descending)
        sorted_students = sorted(students, key=lambda s: s.mark, reverse=True)

        # Find unique enrolled courses
        unique_enrolled_course = []
        all_enrolled_courses = [course for student in students for course in student.enrolled_courses]
        course_count = Counter(course.course_id for course in all_enrolled_courses)
        for course in all_enrolled_courses:
            if course_count[course.course_id] == 1:
                unique_enrolled_course.append(course)

        # Print dashboard
        print(dedent(f"""
            ---------> Summary Dashboard <---------
                         
            Total users: {total_users}
            Total students: {total_students}
            Total courses: {total_courses}
            Total payments: {total_payments}
            Total revenue: {total_revenue}
                       
        """))

        print("---------> Passed Students <---------")
        for student in passed_students():
            print()
            print(f"Student Name: {student.name}")
            print(f"Student Email: {student.email}")
            print(f"Student Mark: {student.mark}")
            print(f"Student Grade: {student.grade}")
            print()

        print("---------> Failed Students <---------")
        for student in failed_students():
            print()
            print(f"Student Name: {student.name}")
            print(f"Student Email: {student.email}")
            print(f"Student Mark: {student.mark}")
            print(f"Student Grade: {student.grade}")
            print()

        print(f"Average Mark: {average_mark}")
        print()
        
        if topper:
            print("---------> Topper <---------")
            print()
            print(f"Student Name: {topper.name}")
            print(f"Student Email: {topper.email}")
            print(f"Student Mark: {topper.mark}")
            print(f"Student Grade: {topper.grade}")
            print()
        
        if expensive_course:
            print("---------> Expensive Course <---------")
            print()
            print(f"Course Name: {expensive_course.name}")
            print(f"Course Fee: {expensive_course.fee}")
            print(f"Course Duration(In weeks): {expensive_course.duration_weeks}")
            print()

        print("---------> Students Sorted By Marks <---------")
        for student in sorted_students:
            print()
            print(f"Student Name: {student.name}")
            print(f"Student Email: {student.email}")
            print(f"Student Mark: {student.mark}")
            print(f"Student Grade: {student.grade}")
            print()

        print("---------> Unique Enrolled Courses <---------")
        for course in unique_enrolled_course:
            print()
            print(f"Course Name: {course.name}")
            print(f"Course Fee: {course.fee}")
            print(f"Course Duration(In weeks): {course.duration_weeks}")
            print()
        
        # Return summary as dict for programmatic use
        return {
            "status": True,
            "total_users": total_users,
            "total_students": total_students,
            "total_courses": total_courses,
            "total_payments": total_payments,
            "total_revenue": total_revenue,
            "average_mark": average_mark,
            "topper": topper,
            "expensive_course": expensive_course,
            "sorted_students": sorted_students
        }
