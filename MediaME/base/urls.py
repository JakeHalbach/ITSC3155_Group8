from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.impression, name='impression'), 
    path('accounts/', include('accounts.urls')),
    path('titlePage/<str:pk>/',views.titlePage, name="title-page"),
]
