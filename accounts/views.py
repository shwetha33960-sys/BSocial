from .models import Profile
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from posts.models import Post
from posts.forms import PostForm, CommentForm

from .forms import ForgotPasswordForm, SignInForm, SignUpForm, ProfileForm


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
    profile = request.user.profile

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, "Post published successfully!")
            return redirect("accounts:dashboard")

    else:
        form = PostForm()

    posts = Post.objects.select_related("author").all()

    context = {
    "profile": profile,
    "form": form,
    "comment_form": CommentForm(),
    "posts": posts,
}

    return render(request, "accounts/dashboard.html", context)

@login_required(login_url="accounts:signin")
def edit_profile_view(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:dashboard")

    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        "accounts/edit_profile.html",
        {"form": form}
    )


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
