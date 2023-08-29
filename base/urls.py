from django.urls import path
from .import views

urlpatterns = [

    path('login/', views.LoginPage, name = "login"),

    path('', views.home, name = 'home'),
    path('room/<str:pk>/', views.room, name = 'room'),
    path('create-room/', views.create_room, name = 'create-room'),
    path('update-room/<str:pk>', views.updateRoom, name = 'update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name = 'delete-room')
]
