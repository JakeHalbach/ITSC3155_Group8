from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchForm, RoomForm, MessageForm
from .models import Media, Room, Message, Type, Genre
from accounts.models import Profile
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import requests
from django.contrib.auth.models import User
# Create your views here.

##populate database
def trim(title):
    for i, char in enumerate(title):
        if char == '.':
            index = i
            return index+2
    return 0
##Media.objects.create(title = movies)
# """
def populate(media_types):
    session = requests.Session()
    index = len(Genre.objects.values_list('name', flat = True))-1
    genres = []
    for i in range(index):
        genres.append(str(Genre.objects.values_list('name', flat = True)[i]))
    for genre in genres:
        #genre = Genre.objects.filter(id=1).first()
        my_url = 'https://www.imdb.com/search/title/?genres='
        my_url += genre.lower()
        response = session.get(my_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup =  BeautifulSoup(response.text, 'lxml')
        medias = soup.find_all('li', class_="ipc-metadata-list-summary-item")

        for media in medias[:10]:
            index = trim(media.find('h3', class_ = 'ipc-title__text').text)
            title = media.find('h3', class_ = 'ipc-title__text').text[index:]
            #print(title)
            description = media.find('div', class_ ="ipc-html-content-inner-div").text
            #print(description)
            if 'TV' in (media.find('div', class_="sc-5179a348-6 bnnHxo dli-title-metadata").text):
                thype = media_types.filter(id=2).first()
            else:
                thype = media_types.filter(id=3).first()
            Media.objects.create(title = title, description = description, media_type = thype, genres = Genre.objects.get(name=genre))
    return
# """

def impression(request):
    popular_rooms = Room.objects.annotate(num_participants=Count('participants')).order_by('-num_participants')[:6]
    return render(request, 'base/impression.html', {'popular_rooms': popular_rooms})

@login_required(login_url='login')
def homePage(request):
    user_rooms = Room.objects.filter(host=request.user) | Room.objects.filter(participants=request.user)
    user_rooms = user_rooms.distinct()
    popular_medias = Media.objects.all()[:10]
    favorited_medias = request.user.profile.favorite_titles.all()
    medias = Media.objects.all()
    preferred_genres = request.user.profile.genres.all()
    recommended_medias = Media.objects.filter(genres__in=preferred_genres).distinct()

    context = {
        'user_rooms': user_rooms,
        'popular_medias': popular_medias,
        'favorited_medias': favorited_medias,
        'medias': medias,
        'recommended_medias': recommended_medias,
    }
    return render(request, 'base/home.html', context)

def search_page(request):
    form = SearchForm(request.GET)
    results = Media.objects.all()
    genres = request.GET.getlist('genre')
    media_types = Type.objects.all()
    # populate(media_types)
    #hold = str(Genre.objects.all()[len(Genre.objects.values_list('name', flat = True))-1])
    if form.is_valid():
        q = form.cleaned_data.get('q')
        media_type = form.cleaned_data.get('media_type')
        if q:
            results = results.filter(title__icontains=q)
        if genres:
            results = results.filter(genres__id__in=genres).distinct()
        if media_type:
            results = results.filter(media_type=media_type)
        
        sort_by = request.GET.get('sort')
        if sort_by == 'title':
            results = results.order_by('title')
        elif sort_by == 'popularity':
            results = results.annotate(
                num_participants=Count('rooms__participants')
            ).order_by('-num_participants')
        else:
            results = results.order_by('-created')

    context = {'form': form, 'results': results, 'genres': genres, 'media_types': media_types}
    #context = {'form': form, 'results': results, 'genres': genres, 'hold': hold}
    
    return render(request, 'base/search.html', context)


def create_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RoomForm()

    context = {'form': form}

    return render(request, 'base/room_form.html', context)

def title_page(request, pk):
    media = Media.objects.get(id=pk)
    rooms = media.rooms.all()
    messages = Message.objects.filter(room__media=media)

    active_participants = (
    User.objects
    .filter(message__in=messages)
    .annotate(post_count=Count('message'))
    .order_by('-post_count')[:5]
)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.media = media
            new_message.author = request.user
            new_message.save()
            return redirect('title-page', pk=media.pk)
    else:
        form = MessageForm()

    context = {'media': media, 'rooms': rooms, 'active_participants': active_participants, 'form': form}
    return render(request, 'base/titlePage.html', context)


def room_tab(request, pk, tab):
    valid_tabs = ['reviews', 'characters', 'plot', 'visuals']
    if tab not in valid_tabs:
        return redirect('home')
    
    media = get_object_or_404(Media, id=pk)
    room = get_object_or_404(Room, media=media, tab=tab)
    messages = Message.objects.filter(room=room).order_by('created')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            msg.room = room
            msg.media = media
            msg.save()

            profile = request.user.profile
            profile.interaction_score += 2
            profile.save()

            room.participants.add(request.user)
            return redirect('room-tab', pk=media.id, tab=tab)
    else:
        form = MessageForm()

    context = {'media':media, 'room':room, 'messages':messages, 'form':form}
    return render(request, 'base/room_tab.html', context)


@login_required
def toggle_favorite(request, pk):
    media = get_object_or_404(Media, pk=pk)
    profile = request.user.profile
    user = request.user

    if media in profile.favorite_titles.all():
        profile.favorite_titles.remove(media)
        media.favorited.remove(user)
    else:
        profile.favorite_titles.add(media)
        media.favorited.add(user)
        profile.interaction_score += 1

    return redirect('title-page', pk=media.id)
