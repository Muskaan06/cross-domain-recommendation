import sys
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

sys.path.append("..")
from CrossDomainRecommendation.genre import actual_genres, get_all_genres
from CrossDomainRecommendation.cf_model import genre_rec
from CrossDomainRecommendation.sql import display_song_rec
from CrossDomainRecommendation.spotify_connect import get_track_id
# Create your views here.


def home(request):
    return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists!")
            return redirect('home')

        if len(username) > 50:
            messages.error(request, "Username cannot be more than 50 characters long!")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be alpha-numeric!")
            return redirect('home')

        myuser = User.objects.create_user(username, None, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.save()
        messages.success(request, "Your account has been created successfully!")
        #  TODO: login user here
        #  ask for 3 fav genre, show song recs w max matching genres, ask rating, build user emo
        #  ask for 3 fav songs (optional), rec songs from cluster, ask rating, update user emo
        #  (make this page and redirect)

        return redirect('signin')

    return render(request, 'authentication/signup.html')


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            if user.last_login is None:
                # login(request, user)
                return redirect('select_genres')
            else:
                login(request, user)
                fname = user.first_name
                return render(request, "authentication/index.html", {'fname': fname})
        else:
            messages.error(request, "bad credentials!")
            return redirect('home')

    return render(request, "authentication/signin.html")


def select_genres(request):
    genre_list = actual_genres()
    if request.method == "POST":
        genres = request.POST.get('genres')
        genres = genres.split(',')
        request.session['genres'] = genres
        return redirect('dashboard')

    return render(request, "authentication/select_genres.html", {'genre_list': genre_list})


def dashboard(request):
    genres = request.session.get('genres')
    rec = genre_rec(genres)
    song_list = []
    for recid in rec:
        song_list.append(display_song_rec(recid))

    track_ids=[]
    for track in song_list:
        song = get_track_id(track[0], track[1])
        # while song is None:
        #     song = get_track_id(track[0], track[1])

        track_ids.append(song)

    song_list = json.dumps(song_list)
    track_ids = json.dumps(track_ids)

    ratings=[]
    if request.method == "POST":
        for i in range(10):
            id = 'rating'+str(i+1)
            ratings.append(request.POST.get(id))
        # rating1 = request.POST.get('rating1')
    print("------", ratings)
    request.session['ratings'] = ratings

    return render(request, "authentication/dashboard.html", {'song_list': song_list, 'track_ids': track_ids})


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')




