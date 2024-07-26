from django.urls import path
from .views import *

app_name = 'cal'

urlpatterns = [
    path('home/', home, name = "home"),
    path('home/<int:year>/<int:month>/', home, name='home_with_date'),
    path('home2/<int:year>/<int:month>/<int:day>/', home2, name='home2'),
    path('add_schedule/<int:year>/<int:month>/<int:day>/', add_schedule, name='add_schedule'),
]