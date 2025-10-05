from django import forms
from courses.models import Course, CouponCode

class PaymentConfirmationForm(forms.Form):
    course_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    transaction_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    transaction_id = forms.CharField(max_length=100, required=True, 
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=True,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    original_amount = forms.DecimalField(max_digits=10, decimal_places=2, required=False,
                                       widget=forms.HiddenInput())
    coupon_code = forms.CharField(max_length=20, required=False,
                                widget=forms.HiddenInput())
    coupon_discount = forms.DecimalField(max_digits=10, decimal_places=2, required=False,
                                       widget=forms.HiddenInput(), initial=0)
    mobile_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    screenshot = forms.ImageField(required=True,
                                widget=forms.FileInput(attrs={'class': 'form-control'}))
    course_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    
    def clean_course_id(self):
        course_id = self.cleaned_data.get('course_id')
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                return course_id
            except Exception as exc:
                # Don't raise validation error, just return None
                return None
        return None
    
    def clean_coupon_code(self):
        coupon_code = self.cleaned_data.get('coupon_code')
        course_id = self.cleaned_data.get('course_id')
        
        if coupon_code and course_id:
            try:
                course = Course.objects.get(id=course_id)
                coupon = CouponCode.objects.get(code=coupon_code.upper(), course=course)
                if not coupon.is_valid():
                    raise forms.ValidationError("Coupon is no longer valid.")
                return coupon_code.upper()
            except CouponCode.DoesNotExist:
                raise forms.ValidationError("Invalid coupon code.")
            except Course.DoesNotExist:
                pass
        return coupon_code