from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.utils import timezone
from django.http import JsonResponse
import json
import datetime

# Create your views here.
def checklist(request):
    user_role = request.user.role #자녀/부모 구분
    today = timezone.now()
    linked_users = request.user.followings.all() # 연동된 사용자들
    completed = request.GET.get('completed') or False
    date_str = request.GET.get('date')

    if date_str:
        try:
            today = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            today = timezone.now().date()
    else:
        today = timezone.now().date()
    
    # 현재 사용자와 연동된 사용자들의 ID를 리스트로 저장
    user_ids = [request.user.id] + list(linked_users.values_list('id', flat=True))
    
    # 현재 사용자의 체크리스트와 연동된 사용자들의 체크리스트 가져오기
    todos = Todo.objects.filter(due_date=today, author_id__in=user_ids).distinct()
    return render(request, 'checklist/home.html', {'todos' : todos, 'current_date':today, 'user_role': user_role})

def create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.author = request.user
            todo.save()
            form.save_m2m() # many-to-many 필드 저장
            return redirect('checklist:home')
    else:
        form = TodoForm()

    return render(request, 'checklist/create.html', {'form': form})

def update_todo_status(request, todo_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            todo = Todo.objects.get(id=todo_id)
            todo.completed = data['completed']
            todo.save()
            return JsonResponse({'status': 'success', 'todo_id': todo_id, 'completed': todo.completed})
        except Todo.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Todo not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def detail(request,id):
    todo = get_object_or_404(Todo, id =id)
    return render(request, 'checklist/detail.html', {'todo':todo})

@login_required
def update(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('checklist:home')
    else:
        form = TodoForm(instance=todo)
    
    return render(request, 'checklist/update.html', {'form': form, 'todo': todo})

@login_required
def delete(request, id):
    todo = get_object_or_404(Todo, id=id)
    todo.delete()
    return redirect('checklist:home')