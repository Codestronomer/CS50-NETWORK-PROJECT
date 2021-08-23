from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    objects = UserManager()
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_owner")
    post = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True)

    # Orders post by the time created
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"Post by {self.user}"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)
    location = models.CharField(max_length=300, blank=True)
    joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Profile for user ({self.user.username})"

