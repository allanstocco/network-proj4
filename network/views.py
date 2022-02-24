from django.contrib.auth import authenticate, login, logout
from django.core import paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *


@login_required(login_url='login')
def index(request):
    user = request.user
    
    post = Posts.objects.order_by('-time').all()

    page_number = request.GET.get('page')

    post_paginator = Paginator(post, 10)

    page = post_paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'count': post_paginator.count,
        'page': page,
        "user": user
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        follows = Follow()
        follows.user = user
        follows.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url='login')
def user_profile(request, user):
    user = User.objects.get(id=user)
    template = f"/profile/{request.user.id}"
    post = Posts.objects.order_by('-time').filter(user=user)
    following = Follow.objects.get(user=user)

    page_number = request.GET.get('page')

    post_paginator = Paginator(post, 10)

    page = post_paginator.get_page(page_number)


    return render(request, "network/profile.html", {
        "postUser": post_paginator.count,
        "url": template,
        "user": user,
        "follow": following.follower.all(),
        "following": following.following.all(),
        'page': page
    })


@login_required(login_url='login')
def profile(request):
    user = request.user
    post = User.objects.get(id=user.id)
    if request.method == "POST":

        doc = request.FILES

        post.name = request.POST["userName"]
        post.city = request.POST["userCity"]
        post.birth = request.POST["userBirth"]

        try:
            post.userImage = doc["userImage"]
            post.background = doc["background"]
            post.save()
        except:
            post.save()

        return HttpResponseRedirect(reverse("user_profile", kwargs={'user': user.id}))
    else:
        return render(request, "network/profile.html", {
            "user": user
        })


@login_required(login_url='login')
def posts(request):
    user = request.user
    if request.method == "POST":

        doc = request.FILES

        campo = request.POST["textpost"]
        try:
            upload = doc["upload"]
            post = Posts.objects.create(user=user, field=campo, image=upload)
            post.save()
        except:
            post = Posts.objects.create(user=user, field=campo)
            post.save()
    return HttpResponseRedirect(reverse("index"))


@login_required
@csrf_exempt
def edit_post(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        new_post = request.POST.get('post')
        try:
            post = Posts.objects.get(id=post_id)
            post.field = new_post.strip()
            post.save()
            return JsonResponse({}, status=201)
        except:
            return JsonResponse({}, status=404)

    return JsonResponse({}, status=400)


@login_required
@csrf_exempt
def liked_post(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        status_post = request.POST.get('liked')
        try:
            post = Posts.objects.get(id=post_id)
            if status_post == "on":
                post.likes.add(request.user)
                status_post = "off"
            elif status_post == "off":
                post.likes.remove(request.user)
                status_post = "on"
            post.save()

            return JsonResponse({"status": 201, "status_post":status_post, "likes_counting": post.likes.count()})

        except:
            return JsonResponse({'error': "Post not found", "status": 404})
    return JsonResponse({}, status=400)

@login_required(login_url='login')
def likedposts_page(request, user):

    user = User.objects.get(id=user)

    liked = user.likes.all()

    return render(request, "network/liked.html", {
        "likes": liked,
        "user": user
    })


@csrf_exempt
def follow_post(request):
    if request.method == "POST":
        
        user = request.POST.get('id')
        toggle = request.POST.get('follow')

        if toggle == 'Follow':
            try:
                
                user = User.objects.get(username=user)
                follow = Follow.objects.get(user=request.user)
                follow.following.add(user)
                follow.save()

                follower = Follow.objects.get(user=user)
                follower.follower.add(request.user)
                follower.save()

                return JsonResponse({'status': 201, 'toggle':'Unfollow', "follower": follower.follower.count()}, status=201)
            except:
                return JsonResponse({'error': "not found", "status": 404})
        else:
            try:
                user = User.objects.get(username=user)
                follow = Follow.objects.get(user=request.user)
                follow.following.remove(user)
                follow.save()

                follower = Follow.objects.get(user=user)
                follower.follower.remove(request.user)
                follower.save()

                return JsonResponse({'status':201, 'toggle':'Follow', "follower": follower.follower.count()}, status=201)
            except:
                return JsonResponse({'error': "not found", "status": 404})
        
    return JsonResponse({}, status=400)

@login_required(login_url='login')
def following_page(request):
    
    user = request.user
    follows = Follow.objects.get(user=user)
    followingPost = Follow.objects.get(user=user).following.all()
    post = Posts.objects.filter(user__in=followingPost).order_by('-time')


    page_number = request.GET.get('page')
    post_paginator = Paginator(post, 10)
    page = post_paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "following": follows.following.all(),
        "followers": follows.follower.all(),
        "followingPosts": post_paginator.count,
        'page': page
    })
