from django.contrib import messages
from django.shortcuts import render
from .models import Media
# Create your views here.


def impression(request):
    return render(request, 'base/impression.html')
def titlePage(request, pk):
    media= Media.objects.get(id = pk)
    ##messages.error(request, title)
    context = {'media':media}
    return render(request, 'base/titlePage.html', context)

