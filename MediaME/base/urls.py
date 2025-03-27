from . import views
from django.urls import path


urlpatterns = [
    
    path('', views.home,name="home"),
    path('titlePage/<str:pk>/',views.titlePage, name="title-page"),
]

