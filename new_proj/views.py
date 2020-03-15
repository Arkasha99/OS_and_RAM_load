from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import LoginForm
import psutil
# Create your views here.


@login_required
def load_average(request):
    os_usage1, os_usage5, os_usage15 = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
    return render(request, 'load_average.html', {'load_average1': os_usage1,
                                                 'load_average5': os_usage5,
                                                 'load_average15': os_usage15})


@login_required
def ram(request):
    ram_usage_percent = psutil.virtual_memory().percent
    ram_usage_total = round(psutil.virtual_memory().total*10**-9,2)
    ram_usage_available = round(psutil.virtual_memory().available*10**-9,2)
    ram_usage_used = round(psutil.virtual_memory().used*10**-9,2)
    ram_usage_free = round(psutil.virtual_memory().free*10**-9,2)
    return render(request, 'ram.html', {
        'percent': ram_usage_percent,
        'total': ram_usage_total,
        'available': ram_usage_available,
        'used': ram_usage_used,
        'free': ram_usage_free,
    })


def user_login(request):
    next_page = ''
    if request.GET:
        next_page = request.GET['next']
    if request.user.is_authenticated:
        return HttpResponseRedirect(request.GET['next'])
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    login(request, user)
                    if next_page == '':
                        return redirect('load-average')
                    else:
                        return HttpResponseRedirect(next_page)
        else:
            form = LoginForm()
            return render(request, "login.html", {'form': form})


def logout(request):
    django_logout(request)
    return redirect('login')