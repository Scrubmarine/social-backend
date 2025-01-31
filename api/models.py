from django.contrib.auth.models import User, Group, Permission
from django.db import models

# TODO: Attempt to use custom user to enforce unique emails and other constraints
# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     # username = models.CharField(max_length=150, unique=True)
#     # first_name = models.CharField(max_length=30, blank=True)
#     # last_name = models.CharField(max_length=30, blank=True)
#     # password = models.CharField(max_length=50)
#
#     groups = models.ManyToManyField(
#         Group,
#         related_name='user_groups',
#         blank=True,
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='user_permissions',
#         blank=True,
#     )


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
