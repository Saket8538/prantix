
from django.contrib import admin
from django.urls import path , include
from courses.views import  MyCoursesList,  HomePageView ,verifyPayment ,  coursePage , SignupView , LoginView , signout , checkout
from courses.views.manual_payment import payment_page, payment_confirm, validate_coupon
from courses.views.courses import CoursesListView
from django.views.generic import TemplateView
from courses.views.newsletter import subscribe as newsletter_subscribe
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', HomePageView.as_view() , name = 'home'),
    path('logout', signout , name = 'logout'),
    path('my-courses', MyCoursesList.as_view() , name = 'my-courses'),
    path('courses/', CoursesListView.as_view(), name='courses'),
    path('signup', SignupView.as_view() , name = 'signup'),
    path('login', LoginView.as_view() , name = 'login'),
    path('course/<str:slug>', coursePage , name = 'coursepage'),
    path('check-out/<str:slug>', checkout , name = 'check-out'),
    path('verify_payment', verifyPayment , name = 'verify_payment'),
    path('payments/', payment_page, name='payments'),
    path('payments/<str:slug>/', payment_page, name='payments-course'),
    path('payment-confirm/', payment_confirm, name='payment-confirm'),
    path('api/validate-coupon/', validate_coupon, name='validate-coupon'),
    # Static info pages
    path('about/', TemplateView.as_view(template_name='courses/static_pages/about.html'), name='about'),
    path('careers/', TemplateView.as_view(template_name='courses/static_pages/careers.html'), name='careers'),
    path('privacy/', TemplateView.as_view(template_name='courses/static_pages/privacy.html'), name='privacy'),
    path('terms/', TemplateView.as_view(template_name='courses/static_pages/terms.html'), name='terms'),
    path('newsletter/subscribe/', newsletter_subscribe, name='newsletter-subscribe'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)