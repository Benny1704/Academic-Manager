from models import Student, Payment
from services import StudentService, PaymentService

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
