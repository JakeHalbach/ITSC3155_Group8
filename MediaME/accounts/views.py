from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .forms import SignupFormStep1, SignupFormStep2

# Create your views here.

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'accounts/profile.html', context)



def signup_step1(request):
    if request.method == 'POST':
        form = SignupFormStep1(request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['username']
            request.session['email'] = form.cleaned_data['email']
            request.session['password'] = form.cleaned_data['password']
            return redirect('signup_step2')
    else:
        form = SignupFormStep1()
    return render(request, 'accounts/signup_step1.html', {'form': form})

def signup_step2(request):
    if request.method == 'POST':
        form = SignupFormStep2(request.POST)
        if form.is_valid():

            user = User.objects.create_user(
                username = request.session['username'],
                email = request.session['email'],
                password = request.session['password1'],
            )

            user.profile.genres = form.cleaned_data['genres']
            user.profile.media_types = form.cleaned_data['media_types']
            user.profile.save()

            del request.session['username']
            del request.session['email']
            del request.session['password']

            messages.success(request, 'Your account has been created!')
            return redirect('login')
    else:
        form = SignupFormStep2()
    return render(request, 'accounts/signup_step2.html', {'form': form})

def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'This username or password is not valid')
        else:
            messages.error(request, 'Invalid login credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_page(request):
    logout(request)
    return redirect('home')
