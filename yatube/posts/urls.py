from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("group/<slug:slug>/", views.group_posts, name="group_posts"),
    path("create/", views.post_create, name="post_create"),
    path("posts/<int:post_id>/edit/", views.post_edit,
         name="post_edit"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("posts/<int:post_id>/", views.post_detail, name="post"),
    path("<str:username>/<int:post_id>/comment/", views.add_comment,
         name="add_comment"),
]
