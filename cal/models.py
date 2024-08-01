from django.db import models
from accounts.models import User

class Schedule(models.Model):
    TITLE_CHOICES = (
        ('진료', '진료'),
        ('입원', '입원'),
        ('처방', '처방'),
    )
    
    title = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    related_words = models.CharField(max_length=10)  # CSV 형태로 저장
    author = models.ForeignKey(to = User, on_delete=models.CASCADE, related_name="schedules")

    def __str__(self):
        return self.title