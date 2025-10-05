from django.db import models
from courses.models import Course, UserCourse
from django.contrib.auth.models import User

class ManualPayment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    )
    
    transaction_id = models.CharField(max_length=100, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    original_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Original price before coupon discount")
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Discount applied from coupon")
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    transaction_date = models.DateField(null=True, blank=True)
    screenshot = models.ImageField(upload_to='files/payment_screenshots')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    coupon_used = models.ForeignKey('CouponCode', on_delete=models.SET_NULL, null=True, blank=True, help_text="Coupon used for this payment")
    user_course = models.ForeignKey(UserCourse, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    admin_remarks = models.TextField(blank=True, null=True)
    
    def __str__(self):
        course_name = self.course.name if self.course else "Manual Payment"
        return f"{self.user.username} - {course_name} - {self.transaction_id}"
    
    @property
    def total_savings(self):
        """Calculate total savings from course discount + coupon discount"""
        course_discount = 0
        if self.course and self.original_amount:
            course_discount = self.course.price - float(self.original_amount)
        return course_discount + float(self.coupon_discount)