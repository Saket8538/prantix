from django.db import models
from django.utils import timezone
from datetime import timedelta
import math
import pytz

def one_year_from_now():
    """Return timezone-aware datetime one year from now in IST"""
    # Get current time in IST
    ist = pytz.timezone('Asia/Kolkata')
    now = timezone.now().astimezone(ist)
    return now + timedelta(days=365)

class Course(models.Model):
    name = models.CharField(max_length = 100 , null = False)
    slug = models.CharField(max_length = 50 , null = False , unique = True)
    description = models.CharField(max_length = 200 , null = True)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False , default = 0) 
    active = models.BooleanField(default = True)
    thumbnail = models.ImageField(upload_to = "files/thumbnail") 
    date = models.DateTimeField(auto_now_add= True) 
    resource = models.FileField(upload_to = "files/resource")
    length = models.IntegerField(null=False)

    def __str__(self):
        return self.name


class CourseProperty(models.Model):
    description  = models.CharField(max_length = 200 , null = False)
    course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)

    class Meta : 
        abstract = True



class Tag(CourseProperty):
    pass
    
class Prerequisite(CourseProperty):
    pass

class Learning(CourseProperty):
    pass

class CouponCode(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    )
    
    code = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='coupons')
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    discount_value = models.IntegerField(default=0, help_text="Percentage (0-100) or Fixed amount")
    max_uses = models.IntegerField(default=1, help_text="Maximum number of times this coupon can be used")
    used_count = models.IntegerField(default=0, help_text="Number of times this coupon has been used")
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField(default=one_year_from_now)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.code} - {self.course.name}"
    
    def is_valid(self):
        """Check if coupon is valid for use (timezone-aware)"""
        from django.utils import timezone
        import pytz
        
        # Get current time in IST
        ist = pytz.timezone('Asia/Kolkata')
        now = timezone.now().astimezone(ist)
        
        # Ensure valid_from and valid_to are timezone-aware in IST
        valid_from_ist = self.valid_from.astimezone(ist) if timezone.is_aware(self.valid_from) else ist.localize(self.valid_from)
        valid_to_ist = self.valid_to.astimezone(ist) if timezone.is_aware(self.valid_to) else ist.localize(self.valid_to)
        
        return (
            self.active and 
            valid_from_ist <= now <= valid_to_ist and
            self.used_count < self.max_uses
        )
    
    def calculate_discount(self, original_price):
        """Calculate discount amount based on type"""
        if not self.is_valid():
            return 0
            
        if self.discount_type == 'percentage':
            # Floor the discount amount to avoid decimals
            return math.floor(original_price * (self.discount_value / 100))
        else:  # fixed
            return min(self.discount_value, original_price)  # Can't discount more than price
    
    def apply_discount(self, original_price):
        """Apply discount and return final price"""
        discount_amount = self.calculate_discount(original_price)
        # Ensure final price is an integer rupee amount (floor)
        return max(0, int(math.floor(original_price - discount_amount)))
    
    class Meta:
        verbose_name = "Coupon Code"
        verbose_name_plural = "Coupon Codes"