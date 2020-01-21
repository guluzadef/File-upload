from django.urls import path
from .views import register,index,addfile,user_login,logout_view,Detail

urlpatterns = [
    path('',index,name='index'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add/', addfile, name='add'),
    path('detail/<int:id>', Detail, name='detail'),


]
