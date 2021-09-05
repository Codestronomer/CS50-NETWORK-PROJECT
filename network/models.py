from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth import get_user_model
from django.db import models
from .utils import resize_image


class User(AbstractUser):
    objects = UserManager()
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_owner")
    post = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    liked = models.ManyToManyField(User, blank=True, default=None, related_name="liked_post")

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"

        # Orders post by the time created
        ordering = ('-created',)

    def __str__(self):
        return f"Post by {self.user}"

    @property
    def num_likes(self):
        return self.liked.all().count()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="profile_pics", blank=True)
    location = models.CharField(max_length=300, blank=True)
    joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Profile for user ({self.user.username})"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="commented by")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(blank=False)
    liked = models.ManyToManyField(User, blank=True, default=None, related_name="liked_comment")
    date = models.DateTimeField(auto_now_add=True, null=False, verbose_name="commented on")

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ('date',)

    def __str__(self):
        return f"Comment {self.id} made by {self.user} on post {self.post_id} on {self.date.strftime('%d %b %Y %H:%M:%S')}"


class Liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = "liked_by")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = "likes", null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name = "likes", null=True, blank=True)

    class Meta:
        unique_together = [['user', 'post'], ['user', 'comment']]


# Defines user following relationship
class Contact(models.Model):
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rel_to_set",  verbose_name = "followed")
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rel_from_set" ,verbose_name = "followed_by")
    created = models.DateTimeField(auto_now_add=True, null=False, verbose_name ="followed on", db_index=True)

    def __str__(self):
        return f"{self.user_from} followed {self.target_user}"

    def get_user_following_posts(self):
        # return posts of users followed by the target user

        return self.target_user.posts.order_by('-created').all()

user_model = get_user_model()
user_model.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name="followers", symmetrical=False))
