from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth.forms import AuthenticationForm # 로그인
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout

# 임시페이지
def comming_soon(request):
    return render(request, 'accounts/comming_soon.html')

def index(request):
    return render(request, 'accounts/index.html')

# 회원가입
def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form' : form})
    form = SignUpForm(request.POST)

    if form.is_valid():
        user = form.save()
        user.is_child = form.cleaned_data['is_child']
        user.is_parent = form.cleaned_data['is_parent']
        user.save()
        return redirect('accounts:index')
    else:
        return render(request, 'accounts/signup.html', {'form' : form})

# 로그인
def login_view(request):
    if request.method == "GET":
        return render(request, 'accounts/login.html', {'form' : AuthenticationForm})

    form = AuthenticationForm(request, data = request.POST)
    if form.is_valid():
        login(request, form.user_cache)
        return redirect('accounts:comming_soon')
    return render(request, 'accounts/login.html', {'form' : form})