from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('comming_soon/', comming_soon, name="comming_soon"), # 임시페이지

    path('index/', index, name = "index"),
    path('signup/', signup_view, name="signup"), # 회원가입
    path('login/', login_view, name="login"), # 로그인
    path('logout/', logout_view, name="logout"),

    # 마이페이지
    path('mypage/', mypage, name="mypage"),
    path('myinfo_update/', myinfo_update, name="myinfo_update"),
    path('gearing/<int:id>/', gearing, name='gearing'),
    path('link-account/<int:user_id>/', link_account.as_view(), name='link_account'),
    path('follow-accept/', follow_accept.as_view(), name='follow_accept'),
    path('follow-reject/', follow_reject.as_view(), name='follow_reject'),
    path('unfollow/<int:user_id>/', unfollow, name='unfollow'),
]