from django.shortcuts import render, redirect
from courses.models import Course, Video, Payment, UserCourse
from django.shortcuts import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from prantix.settings import *
from time import time
from django.contrib import messages


@login_required(login_url='/login')
def checkout(request, slug):
    course = Course.objects.get(slug=slug)
    user = request.user
    error = None
    
    try:
        user_course = UserCourse.objects.get(user=user, course=course)
        error = "You are Already Enrolled in this Course"
        messages.warning(request, error)
        return redirect('my-courses')
    except UserCourse.DoesNotExist:
        pass
    
    amount = None
    if error is None:
        amount = course.price - (course.price * course.discount * 0.01)
    
    # If amount is zero, enroll directly
    if amount == 0:
        userCourse = UserCourse(user=user, course=course)
        userCourse.save()
        messages.success(request, f"You have been enrolled in {course.name} course.")
        return redirect('my-courses')
    
    # Redirect to our new manual payment system
    return redirect('payments-course', slug=slug)

@login_required(login_url='/login')
@csrf_exempt
def verifyPayment(request):
    # This function is kept for backward compatibility
    # but redirects to the new payment system
    messages.info(request, "We have updated our payment system. Please use the new payment method.")
    return redirect('payments')
        
        
 
