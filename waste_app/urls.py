from django.urls import path
from .views import *

urlpatterns = [
    path('',user_login,name='login'),
    path('register/',user_register,name='register'),
    path('logout/', logout_view, name='logout'),
    path('complaint/',complaint_list,name='complaint_list'),
    path('complaint_form',complaint_form,name='complaint_form'),
]

