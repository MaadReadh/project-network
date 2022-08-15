import json
from urllib import response
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


from network.forms import PostForm

from .models import Follow, Post, User


def index(request):
    posts = Post.objects.all().order_by('-creation_date')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    paginated_posts = paginator.get_page(page)
    form = PostForm()
    context = {
        'post_form': form,
        'paginated_posts': paginated_posts,
    }
    return render(request, "network/index.html",context)

@login_required
def profile(request,id):
    user = User.objects.get(id=id)
    posts = Post.objects.filter(user=user).order_by('-creation_date')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    paginated_posts = paginator.get_page(page)
    form = PostForm()
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower = request.user, following = user).exists()
    context = {
        'user_to_show': user,
        'paginated_posts': paginated_posts,
        'post_form': form,
        'is_following': is_following,
    }
    return render(request, "network/profile.html",context)


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            
    return redirect('index')

@login_required
def following(request):
    follows = Follow.objects.filter(follower = request.user)
    posts = Post.objects.filter(user__in = follows.all().values_list('following')).order_by('-creation_date')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    paginated_posts = paginator.get_page(page)
    form = PostForm()
    context = {
        'post_form': form,
        'paginated_posts': paginated_posts,
    }
    return render(request, "network/following.html",context)




@csrf_exempt
@login_required
def edit_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post = Post.objects.get(id= data.get('post_id'))
        if request.user == post.user:
            post.content = data.get('content')
            post.save()

    return JsonResponse({})

@csrf_exempt
@login_required
def like(request):
    data = json.loads(request.body)
    post = Post.objects.get(id = data.get('id'))
    liked = False
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        post.likes_count -= 1
    else:
        post.likes.add(request.user)
        post.likes_count += 1
        liked = True
    post.save()

    return JsonResponse({
            "likes_count": post.likes_count,
            "liked": liked,
    })

@csrf_exempt
@login_required
def follow(request):
    data = json.loads(request.body)
    user = User.objects.get(id = data.get('id'))
    if request.user != user:
        follow = Follow.objects.filter(follower = request.user, following = user)
        if follow.exists():
            print('user in request.user.follow.all()')
            follow.delete()
            request.user.followings_count -= 1
            user.followers_count -= 1
        else:
            print('user not in request.user.follow.all()')
            follow = Follow()
            follow.follower = request.user
            follow.following = user
            follow.save()
            request.user.followings_count += 1
            user.followers_count += 1

    request.user.save()
    user.save()
    return JsonResponse({})
