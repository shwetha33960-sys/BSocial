from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ForgotPasswordForm, SignInForm, SignUpForm


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully.")
            return redirect("accounts:dashboard")
    else:
        form = SignUpForm()

    return render(request, "accounts/auth_page.html", {"form": form, "mode": "signup"})


def signin_view(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect("accounts:dashboard")
    else:
        form = SignInForm()

    return render(request, "accounts/auth_page.html", {"form": form, "mode": "signin"})


@login_required(login_url="accounts:signin")
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")


@login_required(login_url="accounts:signin")
def signout_view(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("accounts:signin")


def forgot_password_view(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            messages.success(request, "If an account exists for that email, you will receive guidance shortly.")
            return redirect("accounts:signin")
    else:
        form = ForgotPasswordForm()

    return render(request, "accounts/forgot_password.html", {"form": form})
