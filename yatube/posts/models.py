from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    objects = None
    text = models.TextField(blank=False, verbose_name="Текст",
                            help_text="Введите текст")
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name="Дата публикации")
    author = models.ForeignKey(User, verbose_name="Автор",
                               on_delete=models.CASCADE,
                               related_name="posts")
    group = models.ForeignKey("Group", blank=True, null=True,
                              on_delete=models.SET_NULL, related_name="posts",
                              verbose_name="Группа для поста",
                              help_text="Выберите группу")
    image = models.ImageField(upload_to="posts/media", blank=True, null=True)


class Meta:
    ordering = ["-pub_date"]
    verbose_name_plural = "Записи"
    verbose_name = "Запись"


class Group(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=200)
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Группы"
        verbose_name = "Группа"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments",
                             verbose_name="Запись")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments",
                               verbose_name="Автор")
    text = models.TextField(verbose_name="Текст",
                            help_text="Введите текст")
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name="Дата комментария")

    class Meta:
        verbose_name_plural = "Комментарии"
