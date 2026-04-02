from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Case, When, IntegerField



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
            if user.profile.role=='admin':
                messages.success(request,'Admin login Successfull')
                return redirect('admin_dashboard')
            else:
                messages.success(request,'User login successfully')
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
    form=ComplaintForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        complaint = form.save(commit=False)
        complaint.user = request.user
        complaint.save()
        #send mail

        send_mail(
            "Complaint Submitted",
            f"Hi,{request.user.username},Your complaint has been Submitted Successfully",
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=True,
        )
        return redirect('complaint_list')
    return render(request, 'waste_app/complaint_form.html', {'form': form})

@login_required
def complaint_list(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'waste_app/complaint_list.html', {'complaints': complaints})


@login_required
def admin_dashboard(request):

    if request.user.profile.role != 'admin':
        return HttpResponse("Unauthorized", status=403)
    
    if request.method == "POST":
        cid = request.POST.get("cid")
        status = request.POST.get("status")

        complaint = Complaint.objects.get(id=cid)
        complaint.status = status
        complaint.save()

        # SEND EMAIL TO USER
        send_mail(
            "Complaint Status Updated",
            f"Your complaint status has been updated to: {status}",
            settings.EMAIL_HOST_USER,
            [complaint.user.email],
            fail_silently=True,
        )

    sort = request.GET.get('sort')

    complaints = Complaint.objects.all()

    # SORTING LOGIC
    if sort == 'pending':
        complaints = complaints.filter(status='Pending').order_by('-created_at')

    elif sort == 'resolved':
        complaints = complaints.filter(status='Resolved').order_by('-created_at')

    else:
        # default sorting (latest first)
        complaints = complaints.order_by('-created_at')


    return render(request, "waste_app/admin_dashboard.html", {
        "complaints": complaints
    })
