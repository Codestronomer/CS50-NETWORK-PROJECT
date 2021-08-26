from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
import json

from .models import User, Post, Profile, Liked, Comment
from .forms import ProfileEditForm, UserEditForm


def index(request):
    posts = Post.objects.all()
    return render(request, "network/index.html", {"posts": posts})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile.objects.create(user=user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# Creates a new post 
@login_required()
def new_post(request):
    if request.method == "POST":
        post = request.POST["post"]
        user = request.user
        Post.objects.create(post=post, user=user)
        return redirect('/')
    else:
        return render(request, "networks/index.html")


# Renders user profile
def profile_view(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(user=user)
    return render(request, "network/profile.html", {"profile": profile, "posts": posts})


@login_required()
# edits profile
def edit_profile(request):
    if request.method == "POST":
        # Update username and email and save
        user = request.user
        username = request.POST['username']
        email = request.POST['email']
        user_obj = User.objects.get(username=request.user)
        user_obj.username = username
        user_obj.email = email
        user_obj.save(update_fields=['username', 'email'])

        # Updates profile and save
        date_of_birth = request.POST['date_of_birth']
        bio = request.POST['bio']
        location = request.POST['location']
        file = request.FILES
        Profile.objects.filter(user=user).update(date_of_birth=date_of_birth, photo=file, location=location, bio=bio)

        messages.success(request, 'Profile updated successfully')
        return redirect(reverse('profile', args=[username]))
    else:
        # Instantiate form with initial values
        user = User.objects.get(username=request.user)
        username = user.username
        email = user.email
        user_form = UserEditForm(initial={'username': username, 'email': email})

        profile = Profile.objects.get(user=request.user)
        bio = profile.bio
        location = profile.location
        date_of_birth = profile.date_of_birth
        profile_form = ProfileEditForm(initial={'bio':bio, 'location': location, 'date_of_birth': date_of_birth})
        return render(request, "network/edit_profile.html", {"profile_form": profile_form, 'user_form': user_form})



@login_required()
def like_view(request):
    user = request.user
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    post_id = data.get("post_id")
    print(post_id)
    likedpost = Post.objects.get(id=post_id)
    if user in likedpost.liked.all():
        likedpost.liked.remove(user)
        like = Liked.objects.get(user=user, post=likedpost)
        like.delete()
    else:
        like = Liked.objects.get_or_create(post=likedpost, user=user)
        likedpost.liked.add(user)
        likedpost.save()
    return  JsonResponse({'success': "Post like successful"}, status=200)