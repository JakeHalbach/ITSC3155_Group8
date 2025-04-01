from django.urls import path
from . import views

urlpatterns = [
    path('signup/step1/', views.signup_step1, name = 'signup_step1'),
    path('signup/step2/', views.signup_step2, name = 'signup_step2'),

    path('login/', views.login_page, name = 'login'),
    path('logout/', views.logout_page, name = 'logout'),
]