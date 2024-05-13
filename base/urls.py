from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logOut,name="logout"),
    path('register/',views.registerUser,name="register"),
    path('profile/<str:pk>/',views.userprofile,name="user-profile"),
    path('rooms/<str:pk>/',views.room,name='room'),
    path('create-room/',views.createroom,name="create-room"),
    path('update-room/<str:pk>/',views.updateroom,name="update-room"),
    path('delete-room/<str:pk>/',views.deleteroom,name="delete-room"),
    path('delete-message/<str:pk>',views.deletemessage,name="delete-message"),
]
