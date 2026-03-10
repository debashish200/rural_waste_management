from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'login Successfull')
            return redirect('complaint_list')
        else:
            messages.error(request,"invalid unsername or password")

    return render(request,'waste_app/login.html')

def logout_view(request):
    logout(request)
    messages.success(request,'Logout Successfully')
    return redirect('login')

@login_required
def complaint_form(request):
    form=ComplaintForm(request.POST or None)

    if form.is_valid():
        complaint = form.save(commit=False)
        complaint.user = request.user
        complaint.save()
        return redirect('complaint_list')
    return render(request, 'waste_app/complaint_form.html', {'form': form})

@login_required
def complaint_list(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'waste_app/complaint_list.html', {'complaints': complaints})


@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect('complaint_list')

    if request.method == "POST":
        cid = request.POST.get("cid")
        status = request.POST.get("status")

        Complaint.objects.filter(id=cid).update(status=status)

    complaints = Complaint.objects.all()

    return render(
        request,
        "waste_app/admin_dashboard.html",
        {"complaints": complaints}
    )