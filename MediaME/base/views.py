from django.shortcuts import render
from .models import media
# Create your views here.

def home(request):
    context = {}
    return render(request, 'base/home.html', context)

def titlePage(request, pk):
    title= media.objects.get(id=pk)
    context = {'title':title}
    return render(request, 'base/titlePage.html', context)


