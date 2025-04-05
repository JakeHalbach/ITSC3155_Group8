from django.contrib import messages
from django.shortcuts import render
from .forms import SearchForm
from .models import Media
# Create your views here.


def impression(request):
    return render(request, 'base/impression.html')

def titlePage(request, pk):
    title= Media.objects.get(id = pk)
    messages.error(request, title)
    context = {'title':title}
    return render(request, 'base/titlePage.html', context)

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