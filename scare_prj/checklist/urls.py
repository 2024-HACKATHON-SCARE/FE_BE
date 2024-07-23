from django.urls import path
from .views import *

app_name = 'checklist'

urlpatterns = [
    path('', checklist, name='home'),
    path('create/', create, name='create'),
    path('update_todo_status/<int:todo_id>/', update_todo_status, name='update_todo_status'),
    path('detail/<int:id>/', detail, name= "detail"),
    path('update/<int:todo_id>/', update, name="update"),
    path('delete/<int:id>/', delete, name="delete"),
]