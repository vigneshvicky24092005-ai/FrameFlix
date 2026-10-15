
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app1.models import *


def main(request):
    return render(request, 'main.html')


def signup_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('signup')

        user= User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            'Account created successfully!'
        )
        login(request, user)
        

    return redirect('home')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')

        messages.error(request, 'Invalid username or password.')
        return redirect('main')

    return redirect('home')


def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return redirect('main')


@login_required
def home(request):
    movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies})


@login_required
def movies_list(request):
    movies = Movie.objects.all()

    saved_movie_ids = MyList.objects.filter(
        user=request.user
    ).values_list('movie_id', flat=True)

    return render(
        request,
        'movie.html',
        {
            'movies': movies,
            'saved_movie_ids': saved_movie_ids,
        }
    )


@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    is_saved = MyList.objects.filter(
        user=request.user,
        movie=movie
    ).exists()

    return render(
        request,
        'movie_detail.html',
        {
            'movie': movie,
            'is_saved': is_saved,
        }
    )


@login_required
def my_list(request):
    saved_movies = MyList.objects.filter(
        user=request.user
    ).select_related('movie', 'movie__genre')

    return render(
        request,
        'my_list.html',
        {'saved_movies': saved_movies}
    )


@login_required
def add_to_my_list(request, movie_id):
    if request.method != 'POST':
        return redirect('movies')

    movie = get_object_or_404(Movie, id=movie_id)

    saved_movie, created = MyList.objects.get_or_create(
        user=request.user,
        movie=movie
    )

    if created:
        messages.success(request, 'Movie added to My List!')
    else:
        messages.info(request, 'Movie is already in My List.')

    return redirect('movies')


@login_required
def remove_from_my_list(request, movie_id):
    if request.method != 'POST':
        return redirect('movies')

    saved_movie = get_object_or_404(
        MyList,
        user=request.user,
        movie_id=movie_id
    )

    saved_movie.delete()
    messages.success(request, 'Movie removed from My List!')

    return redirect('movies')
