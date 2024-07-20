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
        user = form.save(commit=False) # role 추가 변경 가능하도록
        user.role = form.cleaned_data.get('role')
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

# 로그아웃
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('accounts:index')

# 마이페이지
def mypage(request):
    return render(request, 'accounts/mypage.html')

# 나의 정보 수정
def myinfo_update(request):
    info = request.user
    default_image_path = 'default_mypage_image.jpg'

    if request.method == "POST":
        image = request.FILES.get('image')
        info.nickname = request.POST.get('nickname')

        # 기존 이미지가 기본값이 아닌 경우만 삭제
        if info.image.name != default_image_path:
            info.image.delete()

        if image:
            info.image = image

        info.save()
        return redirect('accounts:mypage')
    return render(request, 'accounts/myinfo_update.html', {'info':info})