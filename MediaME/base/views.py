from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchForm, RoomForm, MessageForm
from .models import Media, Room, Message, Type, Genre
from django.db.models import Count
from django.contrib.auth.decorators import login_required
# Create your views here.



def impression(request):
    popular_rooms = Room.objects.annotate(num_participants=Count('participants')).order_by('-num_participants')[:6]
    return render(request, 'base/impression.html', {'popular_rooms': popular_rooms})

@login_required(login_url='login')
def homePage(request):
    user_rooms = Room.objects.filter(host=request.user) | Room.objects.filter(participants=request.user)
    user_rooms = user_rooms.distinct()

    context = {'user_rooms': user_rooms}
    return render(request, 'base/home.html', context)

def search_page(request):
    form = SearchForm(request.GET)
    results = Media.objects.all()
    genres = request.GET.getlist('genre')
    media_types = Type.objects.all()
    
    if form.is_valid():
        q = form.cleaned_data.get('q')
        genre = form.cleaned_data.get('genre')
        media_type = form.cleaned_data.get('media_type')
        if q:
            results = results.filter(title__icontains=q)
        if genre:
            results = results.filter(genres=genre)
        if media_type:
            results = results.filter(media_type=media_type)


    context = {'form': form, 'results': results, 'genres': genres}
    
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

    active_participants = Room.objects.filter(media=media).values('user__username').annotate(post_count=Count('posts')).order_by('-post_count')[:5]

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
    media = get_object_or_404(Media, id=pk)
    room = get_object_or_404(Room, media=media, tab=tab)
    messages = Message.objects.filter(room=room)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            msg.room = room
            msg.media = media
            msg.save()
            room.participants.add(request.user)
            return redirect('room-tab', pk=media.id, tab=tab)
    else:
        form = MessageForm()

    context = {'media':media, 'room':room, 'messages':messages, 'form':form}
    return render(request, 'base/room_tab.html', context)

@login_required
def toggle_favorite(request, pk):
    media = get_object_or_404(Media, id=pk)
    if media.is_favorited(request.user):
        media.favorited.remove(request.user)
    else:
        media.favorited.add(request.user)
    return redirect('title_page', pk=media.id)
