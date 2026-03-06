from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_register(request):
    form=RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    d={'form':form}
    return render(request,'waste_app/register.html',d)

def user_login(request):
    if request.method=='POST':
        user=authenticate(username=request.POST['unsername'],password=request.POST['password'])
        if user:
            login(request,user)
            return redirect('complaint_list')
    return render(request,'waste_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
