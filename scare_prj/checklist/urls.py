from django.urls import path
from .views import *

app_name = 'checklist'

urlpatterns = [
    path('', checklist, name='home'),
    path('<int:todo_id>/update_status/', update_status, name='update_status'),
    path('create/', create, name='create'),
    path('detail/<int:id>/', detail, name= "detail"),
    path('update/<int:todo_id>/', update, name="update"),
    path('delete/<int:id>/', delete, name="delete"),
    path('notification/', notification_list, name="notification")
]