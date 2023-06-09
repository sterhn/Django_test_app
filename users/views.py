from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from users.forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib import messages


# login function
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_posts')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# logout
@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def logout_view(request):
    logout(request)
    return redirect('welcome')

# register
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Hi {username}! Your account has been created! Now login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# profile
@csrf_exempt
@login_required(login_url=reverse_lazy('login'))
def profile(request):
    return render(request, 'profile.html')
