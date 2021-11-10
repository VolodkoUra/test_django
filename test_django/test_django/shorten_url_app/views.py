import pyshorteners
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, LoginForm
from .forms import UrlForm
from .models import Urls


def base(request):
    if request.method == "GET":
        if request.session.get('login'):
            return render(request, 'index.html')
        else:
            return render(request, 'base.html')


def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            # шифрование пароля
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('shorten_url')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'], password=cd['password'])
            if user:
                request.session['login'] = user.username
                print(request.session['login'])
                return redirect('shorten_url')
            else:
                return redirect('user_login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    if request.session.get('login'):
        del request.session['login']  # Удаляем сессию
        return redirect('base')
    else:
        return redirect('base')


# Функция сокращения ссылок
def shorten_url(request):
    urls = Urls.objects.filter(user_id=User.objects.filter(username=request.session.get('login'))[0])
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            url_db = Urls.objects.filter(url_long=cd['url'])
            s = pyshorteners.Shortener()
            url_short = s.tinyurl.short(cd['url'])

            if not url_db:
                new_url_long = Urls.objects.create(url_long=cd['url'], url_short=url_short,
                                                   user_id=User.objects.filter(username=request.session['login'])[0])
                return render(request, 'index.html', {'form': form, 'url_short': url_short, 'urls': urls})
            else:
                url_short = Urls.objects.filter(url_long=cd['url'])[0].url_short
                return render(request, 'index.html', {'form': form, 'url_short': url_short, 'urls': urls})
        else:
            return render(request, 'index.html', {'form': form,
                                                  'massege': 'Введите существующий URL адрес',
                                                  'urls': urls})
    else:
        form = UrlForm()
        return render(request, 'index.html', {'form': form, 'urls': urls})