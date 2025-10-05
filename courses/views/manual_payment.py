from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course, ManualPayment, UserCourse, CouponCode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from courses.forms.payment_form import PaymentConfirmationForm
from django.utils import timezone
import json

@login_required(login_url='/login')
def payment_page(request, slug=None):
    context = {}
    course = None
    
    if slug:
        # If a course slug is provided, show payment for that specific course
        try:
            course = Course.objects.get(slug=slug)
            # Check if user is already enrolled
            try:
                user_course = UserCourse.objects.get(user=request.user, course=course)
                messages.warning(request, "You are already enrolled in this course.")
                return redirect('my-courses')
            except UserCourse.DoesNotExist:
                pass
                
            # Calculate the discounted price (rounded down to integer rupees)
            amount = int(course.price - (course.price * course.discount * 0.01))
            
            # If course is free, enroll directly
            if amount == 0:
                user_course = UserCourse(user=request.user, course=course)
                user_course.save()
                messages.success(request, f"You have been enrolled in {course.name} course.")
                return redirect('my-courses')
                
            context['course'] = course
            context['amount'] = int(amount)
            # Persist selection in session for robust handoff to confirm form
            request.session['payment_course_id'] = course.id
            request.session['payment_amount'] = int(amount)
        except Course.DoesNotExist:
            # Instead of showing error, redirect to payment form without course_id
            messages.info(request, "Please fill in your payment details.")
            return redirect('payment-confirm')
    
    context['upi_id'] = settings.UPI_ID
    # Ensure absolute media URL so it doesn't resolve relative to /payments/<slug>/
    context['qr_code'] = f"{settings.MEDIA_URL}{settings.QR_CODE_IMAGE}" if not settings.QR_CODE_IMAGE.startswith('/') else settings.QR_CODE_IMAGE
    
    return render(request, 'courses/payment_page.html', context)

@login_required(login_url='/login')
def payment_confirm(request):
    if request.method == 'POST':
        form = PaymentConfirmationForm(request.POST, request.FILES)
        if form.is_valid():
            # Get course_id from form
            course_id = form.cleaned_data.get('course_id')
            course = None
            coupon = None
            
            # If course_id is provided, try to get the course
            if course_id:
                try:
                    course = Course.objects.get(id=course_id)
                except Course.DoesNotExist:
                    # Silently handle course not found
                    pass
            
            # Handle coupon validation and usage tracking
            coupon_code = form.cleaned_data.get('coupon_code')
            if coupon_code and course:
                try:
                    coupon = CouponCode.objects.get(code=coupon_code.upper(), course=course)
                    if coupon.is_valid():
                        # Increment usage count
                        coupon.used_count += 1
                        coupon.save()
                    else:
                        # If coupon is not valid, don't apply it
                        coupon = None
                        messages.warning(request, "Coupon code is no longer valid. Payment submitted without discount.")
                except CouponCode.DoesNotExist:
                    # If coupon doesn't exist, continue without it
                    messages.warning(request, "Invalid coupon code. Payment submitted without discount.")
            
            # Create payment record with or without course
            payment = ManualPayment(
                transaction_id=form.cleaned_data['transaction_id'],
                amount=form.cleaned_data['amount'],
                original_amount=form.cleaned_data.get('original_amount') or form.cleaned_data['amount'],
                coupon_discount=form.cleaned_data.get('coupon_discount', 0),
                mobile_number=form.cleaned_data['mobile_number'],
                transaction_date=form.cleaned_data['transaction_date'],
                screenshot=form.cleaned_data['screenshot'],
                user=request.user,
                course=course,
                coupon_used=coupon,
                status='pending'
            )
            payment.save()
            
            # Send email to admin
            course_name = course.name if course else form.cleaned_data.get('course_name', 'Manual Payment')
            subject = f'New payment confirmation request: {course_name}'
            
            # Include coupon information in email context
            email_context = {
                'payment': payment,
                'user': request.user,
                'course': course,
                'course_name': course_name,
                'coupon': coupon,
                'admin_url': request.build_absolute_uri(reverse('admin:courses_manualpayment_change', args=[payment.id]))
            }
            
            html_message = render_to_string('courses/emails/admin_payment_notification.html', email_context)
            plain_message = strip_tags(html_message)
            
            # Send to admin
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  # Send to admin email
                html_message=html_message,
                fail_silently=False,
            )
            
            # Send confirmation to user
            user_subject = 'Payment Verification Submitted'
            user_html_message = render_to_string('courses/emails/user_payment_submitted.html', {
                'payment': payment,
                'course': course,
                'course_name': course_name,
            })
            user_plain_message = strip_tags(user_html_message)
            
            send_mail(
                user_subject,
                user_plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                html_message=user_html_message,
                fail_silently=False,
            )
            
            messages.success(request, "Your payment details have been submitted for verification. We will process it soon.")
            return redirect('my-courses')
        else:
            # Form is invalid: re-render the page with errors and any available course context
            course = None
            course_id = request.POST.get('course_id')
            if course_id:
                try:
                    course = Course.objects.get(id=course_id)
                except Course.DoesNotExist:
                    course = None
            messages.error(request, "Please correct the errors below and resubmit your payment details.")
            context = {'form': form}
            if course:
                context['course'] = course
            return render(request, 'courses/payment_confirm.html', context)
    else:
        # Accept course context via query string or session fallback
        course_id = request.GET.get('course_id') or request.session.get('payment_course_id')
        amount = request.GET.get('amount') or request.session.get('payment_amount')
        original_amount = request.GET.get('original_amount')
        coupon_code = request.GET.get('coupon_code')
        coupon_discount = request.GET.get('coupon_discount', 0)
        
        # Initialize form with empty values if no course is provided
        if not course_id:
            form = PaymentConfirmationForm()
            return render(request, 'courses/payment_confirm.html', {'form': form})
            
        try:
            course = Course.objects.get(id=course_id)
            # Ensure amount is an integer rupee value
            if amount is not None:
                try:
                    amount_int = int(float(amount))
                except Exception:
                    amount_int = int(course.price - (course.price * course.discount * 0.01))
            else:
                amount_int = int(course.price - (course.price * course.discount * 0.01))

            initial_data = {
                'course_id': course_id,
                'amount': amount_int,
                'course_name': course.name
            }
            
            # Add coupon data if available
            if original_amount:
                initial_data['original_amount'] = original_amount
            if coupon_code:
                initial_data['coupon_code'] = coupon_code
            if coupon_discount:
                initial_data['coupon_discount'] = coupon_discount
                
            form = PaymentConfirmationForm(initial=initial_data)
            return render(request, 'courses/payment_confirm.html', {'form': form, 'course': course})
        except Course.DoesNotExist:
            # If course doesn't exist, still show the form without course details
            form = PaymentConfirmationForm()
            return render(request, 'courses/payment_confirm.html', {'form': form})


@csrf_exempt
def validate_coupon(request):
    """AJAX endpoint to validate coupon codes"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            coupon_code = data.get('code', '').strip().upper()
            course_id = data.get('course_id')
            
            # Debug output
            print(f"[DEBUG] Coupon validation request: code={coupon_code}, course_id={course_id}")
            
            if not coupon_code or not course_id:
                return JsonResponse({
                    'valid': False,
                    'message': 'Coupon code and course ID are required.'
                })
            
            try:
                course = Course.objects.get(id=course_id)
                coupon = CouponCode.objects.get(code=coupon_code, course=course)
                print(f"[DEBUG] Coupon found: {coupon.code}, active={coupon.active}, used_count={coupon.used_count}, max_uses={coupon.max_uses}, valid_from={coupon.valid_from}, valid_to={coupon.valid_to}")
                
                if coupon.is_valid():
                    # Calculate original price with course discount
                    original_price = int(course.price - (course.price * course.discount * 0.01))
                    
                    # Calculate coupon discount (already floored in model)
                    coupon_discount_amount = int(coupon.calculate_discount(original_price))
                    final_price = int(coupon.apply_discount(original_price))
                    
                    return JsonResponse({
                        'valid': True,
                        'message': f'Coupon applied successfully! You save ₹{coupon_discount_amount}',
                        'discount_amount': int(coupon_discount_amount),
                        'final_price': int(final_price),
                        'original_price': int(original_price),
                        'discount_type': coupon.discount_type,
                        'discount_value': coupon.discount_value,
                        'coupon_id': coupon.id
                    })
                else:
                    # Check specific reason for invalidity
                    now = timezone.now()
                    if not coupon.active:
                        message = 'This coupon is no longer active.'
                    elif coupon.valid_from > now:
                        message = 'This coupon is not yet valid.'
                    elif coupon.valid_to < now:
                        message = 'This coupon has expired.'
                    elif coupon.used_count >= coupon.max_uses:
                        message = 'This coupon has reached its usage limit.'
                    else:
                        message = 'This coupon is not valid.'
                    
                    return JsonResponse({
                        'valid': False,
                        'message': message
                    })
                    
            except CouponCode.DoesNotExist:
                return JsonResponse({
                    'valid': False,
                    'message': 'Invalid coupon code.'
                })
            except Course.DoesNotExist:
                return JsonResponse({
                    'valid': False,
                    'message': 'Course not found.'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'valid': False,
                'message': 'Invalid request format.'
            })
        except Exception as e:
            return JsonResponse({
                'valid': False,
                'message': 'An error occurred while validating the coupon.'
            })
    
    return JsonResponse({
        'valid': False,
        'message': 'Invalid request method.'
    })