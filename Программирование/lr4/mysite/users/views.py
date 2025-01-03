from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm


def register(request):
   if request.method == 'POST':
       form = UserRegisterForm(request.POST)
       if form.is_valid():
           user = form.save()
           login(request, user)
           messages.success(request, 'Регистрация успешна!')
           return redirect('polls:index')
   else:
       form = UserRegisterForm()
   return render(request, 'users/register.html', {'form': form})
def login_view(request):
   if request.method == 'POST':
       username = request.POST.get('username')
       password = request.POST.get('password')
       user = authenticate(request, username=username, password=password)
       if user is not None:
           login(request, user)
           return redirect('polls:index')
       else:
           messages.error(request, 'Неверное имя пользователя или пароль')
   return render(request, 'users/login.html')
@login_required
def logout_view(request):
   logout(request)
   return redirect('polls:index')