from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, CommentForm
from .models import Post


@login_required(login_url="accounts:signin")
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect("accounts:dashboard")


@login_required(login_url="accounts:signin")
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    return redirect("accounts:dashboard")


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


@login_required(login_url="accounts:signin")
def edit_post(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    if request.method == "POST":
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():
            form.save()
            return redirect("accounts:dashboard")

    else:
        form = PostForm(instance=post)

    return render(
        request,
        "posts/create_post.html",
        {
            "form": form,
        },
    )


@login_required(login_url="accounts:signin")
def delete_post(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    post.delete()

    return redirect("accounts:dashboard")