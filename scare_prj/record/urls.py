from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'record'

urlpatterns = [
    path('', home, name='home'),
    path('create', create, name='create'),
    path('detail/<int:id>/', detail, name='detail'),
    path('update/<int:id>/', update, name = 'update'),
    path('delete/<int:id>/', delete, name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)