from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import PostForm
from .models import Post


@login_required(login_url="accounts:signin")
def create_post_view(request):

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect("accounts:dashboard")

    else:
        form = PostForm()

    return render(
        request,
        "posts/create_post.html",
        {
            "form": form,
        },
    )