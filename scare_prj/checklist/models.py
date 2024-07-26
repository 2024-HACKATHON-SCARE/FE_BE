from django.db import models
from django.conf import settings

class Day(models.Model):
    DAY_CHOICES = [
        ('MO', '월'),
        ('TU', '화'),
        ('WE', '수'),
        ('TH', '목'),
        ('FR', '금'),
        ('SA', '토'),
        ('SU', '일'),
    ]
    day_code = models.CharField(max_length=2, choices=DAY_CHOICES, unique=True)

    def __str__(self):
        return self.get_day_code_display()

    @staticmethod
    def get_day_index(day_code):
        day_index_map = {
            'MO': 0,
            'TU': 1,
            'WE': 2,
            'TH': 3,
            'FR': 4,
            'SA': 5,
            'SU': 6
        }
        return day_index_map.get(day_code, -1)

class Todo(models.Model):
    title = models.CharField(max_length=30)
    due_date = models.DateField(null=True, blank=True)  # 수행해야하는 날짜
    due_time = models.TimeField(null=True, blank=True)  # 수행해야 하는 시간
    repeat_on = models.ManyToManyField(Day, blank=True, related_name='todos')
    completed = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_todos', blank=True) # 연동된 계정끼리 같은 투두 보이기
    
    def __str__(self):
        return f'{self.title} - {self.completed}'