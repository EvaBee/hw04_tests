from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("group", "text",)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("author", "text",)
        help_texts = {"text": "Ваш комментарий"}
        labels = {"text": "Текст комментария"}
