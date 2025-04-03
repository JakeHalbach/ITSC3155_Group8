from django.contrib import messages
from django.shortcuts import render
from .models import Media
# Create your views here.


def impression(request):
    return render(request, 'base/impression.html')
def titlePage(request, pk):
    title= Media.objects.get(id = pk)
    messages.error(request, title)
    context = {'title':title}
    return render(request, 'base/titlePage.html', context)

