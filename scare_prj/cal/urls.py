from django.urls import path
from .views import *

app_name = 'cal'

urlpatterns = [
    path('home/', home, name = "home"),
    path('home/<int:year>/<int:month>/', home, name='home_with_date'),
]