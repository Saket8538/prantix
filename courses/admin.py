from django.contrib import admin
from courses.models import Course, CouponCode, Payment, UserCourse, Tag, Prerequisite, Learning, Video, ManualPayment
from courses.utils.email_utils import send_payment_confirmation_email, send_payment_rejected_email
from django.utils.html import format_html
# Register your models here.

class TagAdmin(admin.TabularInline):
    model = Tag

class VideoAdmin(admin.TabularInline):
    model = Video

class LearningAdmin(admin.TabularInline):
    model = Learning

class PrerequisiteAdmin(admin.TabularInline):
    model = Prerequisite


class CourseAdmin(admin.ModelAdmin):
    inlines = [TagAdmin , LearningAdmin , PrerequisiteAdmin , VideoAdmin]
    list_display = ["name" , 'get_price' , 'get_discount' , 'active']
    list_filter = ("discount" , 'active')

    def get_discount(self , course):
        return f'{course.discount} %'
    
    def get_price(self , course):
        return f'₹ {course.price}'
    
    get_discount.short_description= "Discount"
    get_price.short_description = "Price"

class PaymentAdmin(admin.ModelAdmin):
    model = Payment   
    list_display = [ "order_id" , 'get_user' , 'get_course' , 'status'] 
    list_filter = ["status" , 'course']

    def get_user(self , payment):
        return format_html(f"<a target='_blank' href='/admin/auth/user/{payment.user.id}'>{payment.user}</a>")
    

    def get_course(self , payment):
        return format_html(f"<a target='_blank' href='/admin/courses/course/{payment.course.id}'>{payment.course}</a>")

    get_course.short_description = "Course"
    get_user.short_description = "User"


class UserCourseAdminModel(admin.ModelAdmin):
    model = UserCourse   
    list_display = ['click' , 'get_user' , 'get_course'] 
    list_filter = ['course']

    def get_user(self , usercourse):
        return format_html(f"<a target='_blank' href='/admin/auth/user/{usercourse.user.id}'>{usercourse.user}</a>")
    
    def click(self , usercourse):
        return "Click to Open"
    

    def get_course(self , usercourse):
        return format_html(f"<a target='_blank' href='/admin/courses/course/{usercourse.course.id}'>{usercourse.course}</a>")

    get_course.short_description = "Course"
    get_user.short_description = "User"

admin.site.register(Course , CourseAdmin)
admin.site.register(Video)
admin.site.register(Payment , PaymentAdmin)
admin.site.register(UserCourse , UserCourseAdminModel)

class ManualPaymentAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # If payment is confirmed, ensure UserCourse exists and link it
        if obj.status == 'confirmed':
            from courses.models import UserCourse
            user_course, created = UserCourse.objects.get_or_create(
                user=obj.user,
                course=obj.course
            )
            if obj.user_course != user_course:
                obj.user_course = user_course
                obj.save()
        # Optionally, you can send confirmation email here if needed
    model = ManualPayment
    list_display = ['transaction_id', 'get_user', 'get_course', 'amount', 'get_coupon_info', 'mobile_number', 'transaction_date', 'status', 'date']
    list_filter = ['status', 'course', 'coupon_used']
    search_fields = ['transaction_id', 'user__username', 'course__name', 'coupon_used__code']
    actions = ['mark_as_confirmed', 'mark_as_rejected']
    readonly_fields = ['total_savings']
    
    def get_user(self, payment):
        return format_html(f"<a target='_blank' href='/admin/auth/user/{payment.user.id}'>{payment.user}</a>")
    
    def get_course(self, payment):
        if payment.course:
            return format_html(f"<a target='_blank' href='/admin/courses/course/{payment.course.id}'>{payment.course}</a>")
        return "Manual Payment (No Course)"
    
    def get_coupon_info(self, payment):
        if payment.coupon_used:
            return format_html(
                f"<span style='color: green'>{payment.coupon_used.code}</span><br>"
                f"<small>-₹{payment.coupon_discount}</small>"
            )
        return "-"
    
    def mark_as_confirmed(self, request, queryset):
        for payment in queryset:
            if payment.status != 'confirmed':
                payment.status = 'confirmed'
                payment.save()
                
                # Create UserCourse entry if course exists and not already enrolled
                if payment.course:
                    user_course, created = UserCourse.objects.get_or_create(
                        user=payment.user,
                        course=payment.course
                    )
                    
                    if created:
                        payment.user_course = user_course
                        payment.save()
                        
                    # Send confirmation email to user
                    send_payment_confirmation_email(payment, payment.course, request)
        
        self.message_user(request, f"{queryset.count()} payments marked as confirmed.")
    
    def mark_as_rejected(self, request, queryset):
        for payment in queryset:
            if payment.status != 'rejected':
                payment.status = 'rejected'
                payment.save()
                
                # Send rejection email to user if course exists
                if payment.course:
                    send_payment_rejected_email(payment, payment.course, payment.admin_remarks)
        
        self.message_user(request, f"{queryset.count()} payments marked as rejected.")
    
    mark_as_confirmed.short_description = "Mark selected payments as confirmed"
    mark_as_rejected.short_description = "Mark selected payments as rejected"
    get_course.short_description = "Course"
    get_user.short_description = "User"
    get_coupon_info.short_description = "Coupon Used"

admin.site.register(ManualPayment, ManualPaymentAdmin)

class CouponCodeAdmin(admin.ModelAdmin):
    model = CouponCode
    list_display = ['code', 'get_course', 'discount_type', 'discount_value', 'get_usage', 'get_valid_from_ist', 'get_valid_to_ist', 'active', 'is_currently_valid']
    list_filter = ['discount_type', 'active', 'course', 'valid_from', 'valid_to']
    search_fields = ['code', 'course__name']
    readonly_fields = ['used_count', 'created_date', 'get_ist_times_info']
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'course', 'active')
        }),
        ('Discount Details', {
            'fields': ('discount_type', 'discount_value')
        }),
        ('Usage & Validity', {
            'fields': ('max_uses', 'used_count', 'valid_from', 'valid_to', 'get_ist_times_info')
        }),
        ('Timestamps', {
            'fields': ('created_date',),
            'classes': ('collapse',)
        })
    )
    
    def get_valid_from_ist(self, coupon):
        """Display valid_from in IST"""
        import pytz
        from django.utils import timezone
        ist = pytz.timezone('Asia/Kolkata')
        valid_from_ist = coupon.valid_from.astimezone(ist) if timezone.is_aware(coupon.valid_from) else ist.localize(coupon.valid_from)
        return valid_from_ist.strftime('%d %b %Y, %I:%M %p IST')
    
    def get_valid_to_ist(self, coupon):
        """Display valid_to in IST"""
        import pytz
        from django.utils import timezone
        ist = pytz.timezone('Asia/Kolkata')
        valid_to_ist = coupon.valid_to.astimezone(ist) if timezone.is_aware(coupon.valid_to) else ist.localize(coupon.valid_to)
        return valid_to_ist.strftime('%d %b %Y, %I:%M %p IST')
    
    def get_ist_times_info(self, coupon):
        """Display helpful IST timezone information"""
        import pytz
        from django.utils import timezone
        ist = pytz.timezone('Asia/Kolkata')
        
        valid_from_ist = coupon.valid_from.astimezone(ist) if timezone.is_aware(coupon.valid_from) else ist.localize(coupon.valid_from)
        valid_to_ist = coupon.valid_to.astimezone(ist) if timezone.is_aware(coupon.valid_to) else ist.localize(coupon.valid_to)
        now_ist = timezone.now().astimezone(ist)
        
        return format_html(
            "<div style='background: #f8f9fa; padding: 10px; border-radius: 5px;'>"
            "<strong>🕐 Current IST Time:</strong> {}<br>"
            "<strong>✅ Valid From (IST):</strong> {}<br>"
            "<strong>⏰ Valid To (IST):</strong> {}<br>"
            "<strong>📅 Timezone:</strong> Asia/Kolkata (IST)"
            "</div>",
            now_ist.strftime('%d %b %Y, %I:%M %p'),
            valid_from_ist.strftime('%d %b %Y, %I:%M %p'),
            valid_to_ist.strftime('%d %b %Y, %I:%M %p')
        )
    
    def get_course(self, coupon):
        return format_html(f"<a target='_blank' href='/admin/courses/course/{coupon.course.id}'>{coupon.course.name}</a>")
    
    def get_usage(self, coupon):
        percentage = (coupon.used_count / coupon.max_uses) * 100 if coupon.max_uses > 0 else 0
        color = 'green' if percentage < 50 else 'orange' if percentage < 80 else 'red'
        return format_html(
            f"<span style='color: {color}'>{coupon.used_count}/{coupon.max_uses} ({percentage:.0f}%)</span>"
        )
    
    def is_currently_valid(self, coupon):
        is_valid = coupon.is_valid()
        color = 'green' if is_valid else 'red'
        status = '✓ Valid' if is_valid else '✗ Invalid'
        return format_html(f"<span style='color: {color}'>{status}</span>")
    
    def save_model(self, request, obj, form, change):
        # Ensure code is uppercase
        obj.code = obj.code.upper()
        super().save_model(request, obj, form, change)
    
    get_course.short_description = "Course"
    get_usage.short_description = "Usage"
    get_valid_from_ist.short_description = "Valid From (IST)"
    get_valid_to_ist.short_description = "Valid To (IST)"
    get_ist_times_info.short_description = "IST Times Info"
    is_currently_valid.short_description = "Currently Valid"

admin.site.register(CouponCode, CouponCodeAdmin)
