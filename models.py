from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

class UserRole(Enum):
    ADMIN = "admin"
    STAFF = "staff"
    STUDENT = "student"

class PaymentMethod(Enum):
    CASH = "cash"
    UPI = "upi"
    CARD = "card"

@dataclass
class Course:
    course_id: int
    name: str
    fee: float
    duration_weeks: int

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
    enrolled_courses: list[Course] = field(default_factory=list)

@dataclass
class Payment:
    payment_id: int
    student_id: int
    course_id: int
    amount: int
    payment_method: PaymentMethod
    message: str

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self,amount) -> tuple[str,str]:
        pass

class CashPayment(PaymentStrategy):
    def pay(self, amount) -> tuple[str,str]:
        return "cash", f"paid ₹{amount} using Cash"
    
class UPIPayment(PaymentStrategy):
    def pay(self, amount) -> tuple[str,str]:
        return "upi", f"paid ₹{amount} using UPI"
    
class CardPayment(PaymentStrategy):
    def pay(self, amount) -> tuple[str,str]:
        return "card", f"paid ₹{amount} using Card"
    
