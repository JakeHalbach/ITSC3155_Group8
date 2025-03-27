from django.shortcuts import render
from django.contrib.auth.models import User

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'accounts/profile.html', context)
