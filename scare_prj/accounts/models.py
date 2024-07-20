from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# 이미지 관련 코드
import os
from uuid import uuid4
from django.utils import timezone

# 파일 경로 중복 예방
def upload_filepath(instance, filename):
    today_str = timezone.now().strftime("%Y%m%d")
    file_basename = os.path.basename(filename)
    return f'{instance._meta.model_name}/{today_str}/{str(uuid4())}_{file_basename}'

class User(AbstractUser):
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    role = models.CharField(max_length=10, choices=[('child', '자녀'), ('parent', '부모')], null=False, blank=False)
    nickname = models.CharField(max_length=20, unique=False, blank=True, null=True) # 마이페이지 이름
    image = models.ImageField(upload_to=upload_filepath, blank=True, default='default_mypage_image.jpg') # 마이페이지 프로필 사진
    
    def __str__(self):
        return f'{self.username}'

@receiver(post_save, sender=User)
def set_default_nickname(sender, instance, created, **kwargs):
    if created:
        instance.nickname = instance.username
        instance.save()
