from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from authentication.forms import CustomUserCreationForm
from .models import UserProfile


def register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            address = form.cleaned_data['address']
            age = form.cleaned_data['age']
            phone_number = form.cleaned_data['phone_number']
            # Create a UserProfile for the user
            UserProfile.objects.create(user=user, role=role, address=address, age=age, phone_number=phone_number)
            messages.success(request, "Your account has been successfully created!")
            return redirect("authentication:login")
    context = {"form": form}
    return render(request, "register.html", context)


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("display:display_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)
    context = {"form": form}
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('authentication:login'))
    response.delete_cookie('last_login')
    return response
