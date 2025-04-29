from . import views
from django.urls import path, include



urlpatterns = [
    path('', views.impression, name='impression'),
    path('home/', views.homePage, name='home'),

    path('accounts/', include('accounts.urls')),

    path('search/', views.search_page, name='search-page'),
    path('create-room/', views.create_room, name='create-room'),

    path('media/<int:pk>/', views.title_page, name='title-page'),
    
    path('media/<int:pk>/<str:tab>/', views.room_tab, name='room-tab'),
    
    path('toggle-favorite/<int:pk>/', views.toggle_favorite, name='toggle-favorite'),

]
