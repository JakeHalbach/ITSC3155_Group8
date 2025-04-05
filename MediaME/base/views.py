from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchForm, RoomForm, MessageForm
from .models import Media, Room, Message, User
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

    active_participants = Room.objects.filter(media=media).values('participants__username').annotate(post_count=Count('messages')).order_by('-post_count')[:10]

    context = {'media': media, 'active_participants': active_participants}
    return render(request, 'base/titlePage.html', context)


def room_tab(request, pk, tab):
    media = get_object_or_404(Media, id=pk)
    room = get_object_or_404(Room, media=media, tab=tab)
    messages = Message.objects.filter(room=room)
    participants = User.objects.filter(message__room=room).distinct()
    

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

    context = {'media':media, 'room':room, 'messages':messages, 'form':form, 'participants': participants}
    return render(request, 'base/room_tab.html', context)

def medias_page(request):
    medias = Media.objects.all()
    context = {'medias': medias}
    return render(request, 'base/medias_page.html', context)

