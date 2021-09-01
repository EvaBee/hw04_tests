from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Group, Post, User


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAGINATOR)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(
        request,
        "index.html",
        context
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, settings.PAGINATOR)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "group": group}
    return render(
        request,
        "posts/group_list.html",
        context
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    author_posts_list = author.posts.all()
    paginator = Paginator(author_posts_list, settings.PAGINATOR)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"author": author, "page_obj": page_obj}
    return render(
        request,
        "profile.html",
        context
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(
        request,
        "posts/post_detail.html",
        {"post": post, "author": post.author}
    )


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("profile", username=request.user)
    context = {"form": form}
    return render(
        request,
        "posts/create_post.html",
        context
    )


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    login_author = request.user
    if login_author != post.author:
        return redirect("post", post_id)
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post", post_id)
    return render(
        request,
        "posts/create_post.html",
        {"form": form, "post": post})


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    comments = post.comments.all()
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return(redirect(
            "post", username=username, pk=post_id))
    return render(request,
                  "posts/comments.html",
                  {"form": form, "comments": comments, "post": post}
                  )


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
