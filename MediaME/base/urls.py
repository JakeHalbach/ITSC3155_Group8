from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('titlePage/<str:pk>/',views.titlePage, name="title-page"),
]
