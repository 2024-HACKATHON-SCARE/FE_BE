from django.db import models
from django.contrib.auth.models import AbstractUser
"""
프로필 이미지 관련 코드
import os
from uuid import uuid4
from django.utils import timezone

# 파일 경로 중복 예방
def upload_filepath(instance, filename):
    today_str = timezone.now().strftime("%Y%m%d")
    file_basename = os.path.basename(filename)
    return f'{instance._meta.model_name}/{today_str}/{str(uuid4())}_{file_basename}'
"""

class User(AbstractUser):
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    role = models.CharField(max_length=10, choices=[('child', '자녀'), ('parent', '부모')], null=False, blank=False)
    #mypage_image = models.ImageField(upload_to=upload_filepath, blank=True, default='media/default_mypage_image.jpg')
    
    def __str__(self):
        return f'{self.username}'
