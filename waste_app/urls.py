from django.urls import path
from .views import *

urlpatterns = [
    path('',user_login,name='login'),
    path('register/',user_register,name='register'),
    path('logout/', logout_view, name='logout'),
]

