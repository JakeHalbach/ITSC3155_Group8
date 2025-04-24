from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import SignupFormStep1, SignupFormStep2
from .models import Profile
from base.models import Media


# Create your views here.

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    profile = user.profile
    favorites = Media.objects.filter(favorited=profile.user)
    friends = profile.friends.all()
    context = {'user': user,'profile': profile,'favorites': favorites,'friends': friends}
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
                password = request.session['password'],
            )

            profile = user.profile
            profile.genres.set(form.cleaned_data['genres'])
            profile.media_types.set(form.cleaned_data['media_types'])
            profile.save()

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


@login_required
def toggle_friend(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')

    target_user = get_object_or_404(User, id=user_id)
    user_profile = request.user.profile
    target_profile = target_user.profile

    if target_user in user_profile.friends.all():
        user_profile.friends.remove(target_user)
        target_profile.friends.remove(request.user)
    else:
        user_profile.friends.add(target_user)
        target_profile.friends.add(request.user)

    return redirect('profile', pk=target_user.id)
