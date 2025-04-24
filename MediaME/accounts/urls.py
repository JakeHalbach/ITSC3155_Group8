from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:pk>', views.userProfile, name="user-profile"),
    path('signup/step1/', views.signup_step1, name = 'signup-step1'),
    path('signup/step2/', views.signup_step2, name = 'signup-step2'),

    path('login/', views.login_page, name = 'login'),
    path('logout/', views.logout_page, name = 'logout'),

    path('toggle-friend/<int:user_id>/', views.toggle_friend, name='toggle-friend'),
]