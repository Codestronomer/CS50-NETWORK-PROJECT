from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse
from itertools import chain
import json

from .models import User, Post, Profile, Liked, Comment, Contact
from .forms import ProfileEditForm, UserEditForm


# list all posts by the users
def index(request):
    posts = Post.objects.all()
    profile = Profile.objects.all()

    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {"posts": page_obj})


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
            profile = Profile.objects.create(profile_user=user)
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
        post = request.POST.get("post")
        user = request.user
        Post.objects.create(post=post, user=user)
        return redirect('/')
    else:
        return render(request, "networks/index.html")


# Renders user profile
def profile_view(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(profile_user=user)
    posts = Post.objects.filter(user=user)
    following = Contact.objects.filter(user_from=user)
    total_following = len(following)
    return render(request, "network/profile.html", {
                                                    "profile": profile, 
                                                    "posts": posts,
                                                    "total_following": total_following})


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
        if len(request.FILES) == 1:
            file = request.FILES['photo']
        Profile.objects.filter(profile_user=user).update(date_of_birth=date_of_birth, photo=file, location=location, bio=bio)

        messages.success(request, 'Profile updated successfully')
        return redirect(reverse('profile', args=[username]))
    else:
        # Instantiate form with initial values
        user = User.objects.get(username=request.user)
        username = user.username
        email = user.email
        user_form = UserEditForm(initial={'username': username, 'email': email})

        profile = Profile.objects.get(profile_user=request.user)
        bio = profile.bio
        location = profile.location
        date_of_birth = profile.date_of_birth
        profile_form = ProfileEditForm(initial={'bio':bio, 'location': location, 'date_of_birth': date_of_birth})
        return render(request, "network/edit_profile.html", {"profile_form": profile_form, 'user_form': user_form})



@login_required()
def like_post_view(request):
    user = request.user
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    post_id = data.get("post_id")
    if post_id:
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


@login_required()
def like_comment_view(request):
    user = request.user
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    comment_id = data.get("comment_id")
    if comment_id:
        print(comment_id)
        likedcomment = Comment.objects.get(id=comment_id)
        if user in likedcomment.liked.all():
            likedcomment.liked.remove(user)
            like = Liked.objects.get(user=user, comment=likedcomment)
            like.delete()
        else:
            like = Liked.objects.get_or_create(comment=likedcomment, user=user)
            likedcomment.liked.add(user)
            likedcomment.save()
        return  JsonResponse({'success': "Post like successful"}, status=200)


@login_required()
def comment_view(request):
    user = request.user
    if request.method != "POST":
        return JsonResponse({"error": "Post request required."}, status=400)
    data = json.loads(request.body)
    post_id = data.get("post_id")
    if post_id:
        commented_post = Post.objects.get(id=post_id)
        comment = data.get("content")
        Comment.objects.create(user=user, post=commented_post, content=comment)
        return JsonResponse({'success': 'Comment posted successfully'}, status=200)


# shows the users post that the current user follows.
def following_view(request):
    user_id = request.user.id
    
    # gets the current user
    current_user = User.objects.get(id=user_id)

    # gets the post of the users followed by the current user
    followings = Contact.objects.filter(user_from=current_user)
    posts = Post.objects.all().order_by('created').reverse()
    followed_users_post = []
    for p in posts:
        for user in followings:
            if user.target_user == p.user:
                followed_users_post.append(p)
    if not followings:
        messages.error(request, "Oops! You don't follow anyone.")

    # pagination
    paginator = Paginator(followed_users_post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {"posts": page_obj})

    
@login_required
@require_POST
def follow_view(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Post request required.'})
    data = json.loads(request.body)
    user_id = data.get("user_id")
    action = data.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, target_user=user)
            elif action == "unfollow":
                Contact.objects.filter(user_from=request.user, target_user=user).delete()
            else:
                pass
            return JsonResponse({'status': 'ok'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

