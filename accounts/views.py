from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import UserRegitrationForm

# Create your views here.

def login_user(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            print(request.GET)
            redirect_url = request.GET.get('next','home')
            login(request,user)
            #redirect to home
            return redirect(redirect_url)
        else:
            messages.error(request,'Bad Username or Password')
    return render(request,'accounts/login.htm',context)

@login_required
def logout_user(request):
    logout(request)
    return redirect('accounts:login')

def user_registration(request):
    if request.method == 'POST':
        form = UserRegitrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(username=username,email=email,password=password)
            messages.success(request,f'Thanks for registering {user.username}')
            return redirect('accounts:login')
    else:
        form = UserRegitrationForm()


    return render(request,'accounts/register.htm',{'form':form})