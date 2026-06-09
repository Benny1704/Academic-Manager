from dataclasses import dataclass, field
from enum import Enum

class UserRole(Enum):
    ADMIN = "admin"
    STAFF = "staff"
    STUDENT = "student"

@dataclass
class User:
    user_id: int
    username: str
    email: str
    phone: str
    password: str
    role: UserRole
    is_logged_in: bool = False

@dataclass
class Student:
    student_id: int
    name: str
    age: int
    email: str
    phone: str
    mark: int
    grade: str
    status: str
    enrolled_courses: list[str] = field(default_factory=list)

@dataclass
class Course:
    course_id: int
    name: str
    fee: float
    duration_weeks: int