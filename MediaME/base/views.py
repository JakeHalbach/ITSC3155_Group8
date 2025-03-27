from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')
def titlePage(request, pk):
    title= media.objects.get(id=pk)
    context = {'title':title}
    return render(request, 'base/titlePage.html', context)

