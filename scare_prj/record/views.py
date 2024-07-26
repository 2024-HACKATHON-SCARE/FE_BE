from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone
import datetime


@login_required
def home(request):
    records = Record.objects.filter(user=request.user).order_by('-created_at')
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