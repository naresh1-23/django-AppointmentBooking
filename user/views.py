from django.shortcuts import render, redirect
from .models import UserModel
from bookingapp.models import Appointmentlist
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

def profile(request):
    detail = UserModel.objects.filter(username = request.user.username).first()
    appointments = Appointmentlist.objects.filter(user_id = detail).all()

    return render(request, 'user/profile.html', {'detail':detail, 'appointments': appointments})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        contact = request.POST['contact']
        FirstName = request.POST['first_name']
        LastName = request.POST['last_name']
        hased_pass = make_password(password1)
        if username == '' or email == '' or password1 == '' or password2 == '' or contact == '' or FirstName == '' or LastName == '':
            messages.warning(request, f'Field cannot be empty')
        elif UserModel.objects.filter(username = username).exists():
            messages.warning(request, f'Username already exist')
        elif UserModel.objects.filter(email = email).exists():
            messages.warning(request, f'Email already exist')
        elif password1 != password2:
            messages.warning(request, f"Password didn't matched")
        elif len(str(contact)) != 10:
            messages.warning(request, f'Contact number is not valid')
        else:
            user = UserModel.objects.create(username =username, email = email, first_name = FirstName, last_name = LastName, password = hased_pass, contact = contact)
            user.save()
            messages.success(request, f'Account created. Now you can login')
            return redirect('login')
        return render(request, 'user/register.html')
    else:
        return render(request, 'user/register.html')

def loginuser(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username = username, email = email, password = password)
        if username == '' or email == '' or password == '':
            messages.warning(request, f'Field cannot be empty')
        elif user is not None:
            login(request, user)
            messages.success(request, f'Welcome to homepage { user.first_name }')
            return redirect('home')
        else:
            messages.warning(request, f'Username or password is incorrect')
    return render(request, 'user/login.html')

@login_required
def logoutuser(request):
    logout(request)
    messages.success(request, f'You have been logged out')
    return redirect('home')