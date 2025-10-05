from django.shortcuts import render , redirect
from courses.models import Course , Video , UserCourse
from django.shortcuts import HttpResponse
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.utils.decorators import method_decorator


class CoursesListView(ListView):
    template_name = 'courses/courses_list.html'
    queryset = Course.objects.filter(active=True).order_by('-id')
    context_object_name = 'courses'


@method_decorator(login_required(login_url='login') , name='dispatch')
class MyCoursesList(ListView):
    template_name = 'courses/my_courses.html'
    context_object_name = 'user_courses'
    def get_queryset(self):
        return UserCourse.objects.filter(user = self.request.user)


def coursePage(request , slug):
    course = Course.objects.get(slug  = slug)
    serial_number  = request.GET.get('lecture')
    videos = course.video_set.all().order_by("serial_number")

    if serial_number is None:
        serial_number = 1 

    video = Video.objects.get(serial_number = serial_number , course = course)

    # Check enrollment status first
    user_enrolled = False
    if request.user.is_authenticated:
        try:
            user_course = UserCourse.objects.get(user = request.user, course = course)
            user_enrolled = True
        except UserCourse.DoesNotExist:
            user_enrolled = False

    # Enforce preview restrictions: if video is NOT preview and user is NOT enrolled, deny access
    if not video.is_preview and not user_enrolled:
        if not request.user.is_authenticated:
            return redirect("login")
        else:
            # User is logged in but not enrolled - redirect to checkout
            return redirect("check-out", slug=course.slug)
        
        
    context = {
        "course" : course , 
        "video" : video , 
        'videos':videos
    }
    return  render(request , template_name="courses/course_page.html" , context=context )    
    