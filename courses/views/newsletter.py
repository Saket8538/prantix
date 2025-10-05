from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpRequest, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

@require_POST
def subscribe(request: HttpRequest):
    email = (request.POST.get('email') or '').strip()
    next_url = request.META.get('HTTP_REFERER') or reverse('home')
    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, 'Please enter a valid email address.')
        return HttpResponseRedirect(next_url)

    # Send a simple confirmation email (no DB persistence to keep it non-invasive)
    subject = 'You are subscribed to PrantiX updates'
    html_message = render_to_string('courses/emails/newsletter_welcome.html', {'email': email})
    plain_message = f'Thank you for subscribing to PrantiX updates with {email}. You can unsubscribe anytime.'

    try:
        send_mail(
            subject,
            plain_message,
            getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@prantix.local'),
            [email],
            html_message=html_message,
            fail_silently=True,
        )
        messages.success(request, 'Thanks for subscribing! Welcome to the PrantiX community.')
    except Exception:
        # Fail silently but inform user
        messages.info(request, 'Subscription received. If you do not see a confirmation email, please check spam.')

    return HttpResponseRedirect(next_url)
