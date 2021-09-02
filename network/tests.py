from django.test import TestCase
from .models import User, Post, Contact, Like, Comment

# Create your tests here.
class UserTestCase(TestCase):

    def setUp(self):

        # Create USER.
        a1 = User.objects.create(username="example1", email="example2@example2.com")
        a2 = User.objects.create(username="example1", email="example2@example2.com")

        # Create Post
        post1 = Post.objects.create(user=a1, content="This is a sample text")

        post2 = Post.objects.create(user=a2, content="This is a sample text")

        # Create Like 
        Like1 = Like.objects.create(user=a1, post=post2)
        Like2 = Like.objects.create(user=a2, post= post1)


    def test_valid_post_like(self):
        a1 = User.objects.get(username="example1")
        a2 = User.objects.get(username="example2")
        post2 = Post.objects.create(user=a2, content="This is a sample text")
        f = Like.objects.get(user=a1, post=post2)
        self.assertTrue(f.is_valid_post_like())
