from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth.forms import AuthenticationForm # 로그인
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.http import HttpResponseForbidden, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import FollowSerializer

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


@login_required
def gearing(request, id):
    user = get_object_or_404(User, id=id)
    followers = user.followings.all()
    follow_requests = user.received_follow_requests.filter(status='pending')

    searched = False
    searched_user = None

    if 'gear_id' in request.GET:
        searched = True
        gear_id = request.GET.get('gear_id')
        try:
            searched_user = User.objects.get(username=gear_id)
        except User.DoesNotExist:
            searched_user = None

    return render(request, 'accounts/gearing.html', {
        'follow_requests': follow_requests,
        'followers': followers,
        'searched': searched,
        'searched_user': searched_user
    })


# 계정 연동 신청
class link_account(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        from_user = request.user
        to_user = get_object_or_404(User, id=user_id)
        serializer = FollowSerializer(data={'from_user': from_user.pk, 'to_user': to_user.pk})
        serializer.is_valid(raise_exception=True)
        follow_request = serializer.save()
        return Response({"message": "친구 신청을 보냈습니다."}, status=status.HTTP_201_CREATED)


# 연동 신청 수락
class follow_accept(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        follow_request_id = request.data.get('follow_request_id')
        if not follow_request_id:
            return Response({"message": "follow_request_id가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        follow_request = get_object_or_404(Follow, id=follow_request_id)
        
        if follow_request.to_user != request.user:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        if follow_request.status != 'pending':
            return Response({"message": "이미 처리된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)

        follow_request.status = 'accepted'
        follow_request.save()

        from_user = follow_request.from_user
        to_user = follow_request.to_user

        from_user.followings.add(to_user)
        to_user.followings.add(from_user)


        return Response({"message": "친구 신청을 수락했습니다."}, status=status.HTTP_200_OK)

# 연동 신청 거절
class follow_reject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        follow_request_id = request.data.get('follow_request_id')
        if not follow_request_id:
            return Response({"message": "follow_request_id가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        follow_request = get_object_or_404(Follow, id=follow_request_id)

        if follow_request.to_user != request.user:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        if follow_request.status != 'pending':
            return Response({"message": "이미 처리된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)

        follow_request.status = 'rejected'
        follow_request.save()

        return Response({"message": "친구 신청을 거절했습니다."}, status=status.HTTP_200_OK)


# 연동 삭제
def unfollow(request, user_id):
    current_user = request.user
    user_to_unfollow = get_object_or_404(User, id=user_id)

    if user_to_unfollow in current_user.followings.all():
        current_user.followings.remove(user_to_unfollow)
        return redirect('accounts:gearing', id=current_user.id)
    else:
        return Response({"message": "이미 처리된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)