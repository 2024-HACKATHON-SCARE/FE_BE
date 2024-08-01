from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone
import datetime


@login_required
def home(request):
    linked_users = request.user.followings.all()

    # 현재 사용자와 연동된 사용자들의 ID를 리스트로 저장
    user_ids = [request.user.id] + list(linked_users.values_list('id', flat=True))
    
    # 현재 사용자의 체크리스트와 연동된 사용자들의 체크리스트 가져오기
    records = Record.objects.filter(user_id__in=user_ids).distinct()
    return render(request, 'record/home.html', {'records':records})

@login_required
def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        record = Record.objects.create(
            title = title,
            content = content,
            image = image,
            user = request.user
        )
        record.save()

        return redirect('record:home')
    return render(request, 'record/create.html')

@login_required
def detail(request, id):
    record = get_object_or_404(Record, id = id)
    return render(request, 'record/detail.html', {'record': record})

@login_required
def update(request,id):
    record = get_object_or_404(Record, id=id)
    if request.method == "POST":
        record.title = request.POST.get('title')
        record.content = request.POST.get('content')
        image = request.FILES.get('image')

        if image:
            record.image.delete()
            record.image = image

        record.save()
        return redirect('record:detail', id)
    return render(request, 'record/update.html', {'record': record})

@login_required
def delete(request, id):
    record = get_object_or_404(Record, id=id)
    record.delete()
    return redirect('record:home')