from django.db import models
from accounts.models import User
import os
from uuid import uuid4
from django.utils import timezone

# Create your models here.
def upload_filepath(instance, filename):
    today_str = timezone.now().strftime("%Y%m%d")
    file_basename = os.path.basename(filename)
    return f'{instance._meta.model_name}/{today_str}/{str(uuid4())}_{file_basename}'

class Record(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=upload_filepath, blank = True, null = True)

    def __str__(self):
        return self.title