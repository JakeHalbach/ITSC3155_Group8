from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.impression, name='impression'), 
    path('accounts/', include('accounts.urls')),
    path('titlePage/<str:pk>/',views.titlePage, name="title_page"),
    path('search/', views.search_page, name='search_page'),
]
