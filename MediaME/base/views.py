from django.shortcuts import render


def impression(request):
    return render(request, 'base/impression.html')

