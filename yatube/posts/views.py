from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import PostForm, CommentForm
from .models import Group, Post, User


@cache_page(60 * 20)
def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.PAGINATOR)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "index.html",
        {"page": page}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, settings.PAGINATOR)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "posts/group.html",
        {"group": group, "page": page})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    author_posts_list = author.posts.all()
    paginator = Paginator(author_posts_list, settings.PAGINATOR)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "profile.html",
        {"author": author, "page": page}
    )


def post_view(request, username, post_id):
    post = Post.objects.get(id=post_id, author__username=username)
    comments = post.comments.all()
    form = CommentForm()
    return render(
        request,
        "posts/post.html",
        {"post": post, "author": post.author,
         "comments": comments, "form": form}
    )


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("index")
    return render(
        request,
        "posts/create_or_update_post.html",
        {"form": form}
    )


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    login_author = request.user
    if login_author != post.author:
        return redirect("post", username, post_id)
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("post", username, post_id)
    return render(
        request,
        "posts/create_or_update_post.html",
        {"form": form, "post": post}
    )


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
            "post", username=username, post_id=post_id))
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
