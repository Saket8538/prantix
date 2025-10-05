from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse

def send_payment_confirmation_email(payment, course, request=None):
    """
    Send email to user when their payment is confirmed
    """
    subject = f'Payment Confirmed - Access Granted to {course.name}'
    
    context = {
        'payment': payment,
        'course': course,
    }
    
    if request:
        context['course_url'] = request.build_absolute_uri(reverse('my-courses'))
    else:
        context['course_url'] = '/my-courses'
    
    html_message = render_to_string('courses/emails/user_payment_confirmed.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [payment.user.email],
        html_message=html_message,
        fail_silently=False,
    )
    
def send_payment_rejected_email(payment, course, reason=None):
    """
    Send email to user when their payment is rejected
    """
    subject = f'Payment Verification Failed - {course.name}'
    
    context = {
        'payment': payment,
        'course': course,
        'reason': reason or 'The payment details could not be verified.'
    }
    
    html_message = render_to_string('courses/emails/user_payment_rejected.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [payment.user.email],
        html_message=html_message,
        fail_silently=False,
    )