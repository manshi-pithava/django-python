from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import UserProfile


# HOME PAGE VIEW
def index(request):
    storage = messages.get_messages(request)
    storage.used = True  #  Clears previous messages before rendering
    return render(request, "core_templates/index.html")


# USER REGISTRATION
def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data["username"]).exists():
                messages.error(request, "Username already exists.")
                return redirect("register")

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Ensure UserProfile is created
            UserProfile.objects.get_or_create(user=user, defaults={"role": 2})

            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")  # Redirect to login page instead of auto login
    else:
        form = UserRegistrationForm()

    return render(request, "accounts_templates/register.html", {"form": form})


# USER LOGIN
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.GET.get("next", "index")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

            # Prevent duplicate login messages
            if not any(message.message == "You have been logged in." for message in messages.get_messages(request)):
                messages.success(request, "You have been logged in.")

            # Fetch user profile
            user_profile = UserProfile.objects.filter(user=user).first()

            if user.is_superuser or (user_profile and user_profile.role == 1):  # Admin role
                return redirect("admin_dashboard")  # Redirect to admin panel
            else:
                return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, "accounts_templates/login.html")


# USER LOGOUT
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out.")
    return redirect("login")  # Redirect to login page after logout


# USER PROFILE
@login_required(login_url="login")
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, "accounts_templates/profile.html", {"profile": user_profile})
