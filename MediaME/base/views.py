from django.shortcuts import render
from .models import media
# Create your views here.


def impression(request):
    return render(request, 'base/impression.html')
def titlePage(request, pk):
    title= media.objects.get(id=pk)
    context = {'title':title}
    return render(request, 'base/titlePage.html', context)

