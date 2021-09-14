from django.contrib import admin

from .models import Post, Comment, Contact, User, Profile

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Contact)
admin.site.register(Profile)
admin.site.register(User)