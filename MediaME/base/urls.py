from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.impression, name='impression'), 
    path('accounts/', include('accounts.urls')),
    path('search/', views.search_page, name='search_page'),
    path('create-room/', views.create_room, name='create-room'),

    path('titlePage/<str:pk>/',views.titlePage, name="title_page"),
    path('media/<int:pk>/', views.title_page, name='title-page'),
    
    path('media/<int:media_id>/<str:topic>/', views.room_tab, name='room-tab'),
    
    path('home/', views.homePage, name='home'),
]
