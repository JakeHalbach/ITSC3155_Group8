from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchForm, RoomForm, MessageForm
from .models import Media, Room, Message
from django.db.models import Count
# Create your views here.


def impression(request):
    return render(request, 'base/impression.html')

def search_page(request):
    form = SearchForm(request.GET)
    results = Media.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get('q')
        genre = form.cleaned_data.get('genre')
        media_type = form.cleaned_data.get('media_type')
        if q:
            results = results.filter(title__icontains=q)
        if genre:
            results = results.filter(genre=genre)
        if media_type:
            results = results.filter(media_type=media_type)


    context = {'form': form, 'results': results}
    
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

def titlePage(request, pk):
    title= Media.objects.get(id = pk)
    messages.error(request, title)
    context = {'title':title}
    return render(request, 'base/titlePage.html', context)

def title_page(request, pk):
    media = Media.objects.get(id=pk)

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

    context = {'media': media, 'active_participants': active_participants, 'form': form}
    return render(request, 'base/titlePage.html', context)


def room_tab(request, pk, topic):
    media = get_object_or_404(Media, id=pk)
    room = get_object_or_404(Room, media=media, topic=topic)
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
            return redirect('room-tab', pk=media.id, topic=topic)
    else:
        form = MessageForm()

    context = {'media':media, 'room':room, 'messages':messages, 'form':form}
    return render(request, 'base/room_tab.html', context)

