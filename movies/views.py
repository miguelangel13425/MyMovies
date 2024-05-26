from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Movie
from .forms import NameForm, MovieReviewForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

def index(request):
    movies = Movie.objects.all()
    context = {'movie_list': movies}
    return render(request, "index.html", context=context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if request.method == 'POST':
        form = MovieReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return HttpResponseRedirect(request.path)
    else:
        form = MovieReviewForm()

    reviews = movie.moviereview_set.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    context = {'movie': movie, 'form': form, 'average_rating': average_rating}
    return render(request, 'movie_detail.html', context)

def get_name(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return render(request, "name_ok.html", {"form": form})
        else:
            return render(request, "name_ok.html", {"form": form})
    else:
        form = NameForm()
    return render(request, "name.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
