from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
import calendar
from django.http import HttpResponse
from .models import *
from accounts.models import User

def home(request, year=None, month=None):
    if year is None or month is None:
        today = datetime.today()
        year = today.year
        month = today.month

    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month) # 이번 달 날짜 주별로 리스트
    
    # 이전 달의 년, 월을 계산
    prev_year, prev_month = (year, month - 1) if month > 1 else (year - 1, 12)
    prev_month_days = calendar.monthrange(prev_year, prev_month)[1] # 이전 달 날짜 수

    # 다음 달의 년, 월을 계산
    next_year, next_month = (year, month + 1) if month < 12 else (year + 1, 1)
    
    # 날짜 수정
    for i, week in enumerate(month_days):
        box = 1
        for j, day in enumerate(week):
            if day == 0:
                if i == 0:  # 첫 번째 주
                    month_days[i][j] = (prev_month_days - week.count(0) + 1, 'prev-month')
                elif i == len(month_days) - 1:  # 마지막 주
                    month_days[i][j] = (box, 'next-month')
                    box += 1
            else:
                month_days[i][j] = (day, 'current-month')

    # 한국어 요일과 월을 설정
    weekdays = ["일", "월", "화", "수", "목", "금", "토"]
    
    # 달력에 연동된 일정 뜨도록
    linked_users = request.user.followings.all() # 연동된 사용자들
    # 현재 사용자와 연동된 사용자들의 ID를 리스트로 저장
    user_ids = [request.user.id] + list(linked_users.values_list('id', flat=True))
    month_schedules = Schedule.objects.filter(author_id__in=user_ids).distinct()

    context = {
        'year': year,
        'month': month,
        'cal_rows': month_days,
        'weekdays': weekdays,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'month_schedules': month_schedules,
    }

    return render(request, 'cal/home.html', context)

@login_required
def home2(request, year, month, day):
    """
    달력
    """
    selected_day = day
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month) # 이번 달 날짜 주별로 리스트
    
    # 이전 달의 년, 월을 계산
    prev_year, prev_month = (year, month - 1) if month > 1 else (year - 1, 12)
    prev_month_days = calendar.monthrange(prev_year, prev_month)[1] # 이전 달 날짜 수

    # 다음 달의 년, 월을 계산
    next_year, next_month = (year, month + 1) if month < 12 else (year + 1, 1)
    
    # 날짜 수정
    for i, week in enumerate(month_days):
        box = 1
        for j, day in enumerate(week):
            if day == 0:
                if i == 0:  # 첫 번째 주
                    month_days[i][j] = (prev_month_days - week.count(0) + 1, 'prev-month')
                elif i == len(month_days) - 1:  # 마지막 주
                    month_days[i][j] = (box, 'next-month')
                    box += 1
            else:
                month_days[i][j] = (day, 'current-month')

    # 한국어 요일과 월을 설정
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    selected_weekday_index = calendar.weekday(year, month, selected_day)
    selected_weekday = weekdays[selected_weekday_index]

    """
    일정 확인
    """
    # 달력에 연동된 일정 뜨도록
    linked_users = request.user.followings.all() # 연동된 사용자들
    # 현재 사용자와 연동된 사용자들의 ID를 리스트로 저장
    user_ids = [request.user.id] + list(linked_users.values_list('id', flat=True))

    selected_date = datetime(year = int(year), month = int(month), day = selected_day).date()
    schedules = Schedule.objects.filter(date=selected_date, author_id__in=user_ids).distinct()

    month_schedules = Schedule.objects.filter(author_id__in=user_ids).distinct()

    context = {
        'year': year,
        'month': month,
        'selected_day': selected_day,
        'cal_rows': month_days,
        'weekdays': weekdays,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'selected_weekday': selected_weekday,
        'schedules': schedules,
        'month_schedules': month_schedules,
    }

    return render(request, 'cal/home2.html', context)

@login_required
def add_schedule(request, year, month, day):
    if request.method == 'POST':
        title = request.POST.get('title')
        time_hour = request.POST.get('time_hour')
        time_minute = request.POST.get('time_minute')
        am_pm = request.POST.get('am_pm')
        related_words = request.POST.getlist('related_words')
        additional_word = request.POST.get('additional_word')

        if additional_word:
            related_words.append(additional_word)
        
        time_str = f"{time_hour}:{time_minute} {am_pm}"
        time_obj = datetime.strptime(time_str, '%I:%M %p').time()

        related_words_str = ",".join(related_words)

        schedule = Schedule(
            title=title,
            date=datetime(year, month, day),
            time=time_obj,
            related_words=related_words_str,
            author = request.user,
        )
        schedule.save()
        
        return redirect('cal:home2', year=year, month=month, day=day)

    # 달력에 연동된 일정 뜨도록
    linked_users = request.user.followings.all() # 연동된 사용자들
    # 현재 사용자와 연동된 사용자들의 ID를 리스트로 저장
    user_ids = [request.user.id] + list(linked_users.values_list('id', flat=True))

    # 기존 일정의 관련 단어를 불러오기
    existing_keywords = Schedule.objects.filter(author_id__in=user_ids).values_list('related_words', flat=True)
    unique_keywords = {'진료', '처방', '입원'}
    for keywords in existing_keywords:
        unique_keywords.update(keywords.split(','))

    # 시간과 분의 리스트를 생성하여 context에 추가
    hours = range(1, 13)  # 1부터 12까지
    minutes = range(0, 60)  # 0부터 59까지

    context = {
        'year': year,
        'month': month,
        'day': day,
        'title_choices': Schedule.TITLE_CHOICES,
        'hours': hours,
        'minutes': minutes,
        'existing_keywords': unique_keywords,
    }

    return render(request, 'cal/add_schedule.html', context)

@login_required
def update_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    if request.method == "POST":
        title = request.POST.get('title')
        time_hour = request.POST.get('time_hour')
        time_minute = request.POST.get('time_minute')
        am_pm = request.POST.get('am_pm')
        related_words = request.POST.getlist('related_words')
        additional_word = request.POST.get('additional_word')

        if additional_word:
            related_words.append(additional_word)
        
        time_str = f"{time_hour}:{time_minute} {am_pm}"
        time_obj = datetime.strptime(time_str, '%I:%M %p').time()

        related_words_str = ",".join(related_words)

        schedule.title = title
        schedule.time = time_obj
        schedule.related_words = related_words_str

        schedule.save()

        date = schedule.date
        year = date.year
        month = date.month
        day = date.day
        
        return redirect('cal:home2', year=year, month=month, day=day)

    # 달력에 연동된 일정 뜨도록
    linked_users = request.user.followings.all() # 연동된 사용자들
    # 현재 사용자와 연동된 사용자들의 ID를 리스트로 저장
    user_ids = [request.user.id] + list(linked_users.values_list('id', flat=True))

    # 기존 일정의 관련 단어를 불러오기
    existing_keywords = Schedule.objects.filter(author_id__in=user_ids).values_list('related_words', flat=True)
    unique_keywords = {'진료', '처방', '입원'}
    for keywords in existing_keywords:
        unique_keywords.update(keywords.split(','))

    hours = range(1, 13)  # 1부터 12까지
    minutes = range(0, 60)  # 0부터 59까지

    # 선택된 시간과 분을 12시간 포맷으로 변경
    schedule_time = schedule.time
    selected_hour = schedule_time.hour % 12 or 12
    selected_minute = schedule_time.minute
    selected_am_pm = 'AM' if schedule_time.hour < 12 else 'PM'

    context = {
        'schedule': schedule,
        'title_choices': Schedule.TITLE_CHOICES,
        'hours': hours,
        'minutes': minutes,
        'existing_keywords': unique_keywords,
        'selected_hour': selected_hour,
        'selected_minute': selected_minute,
        'selected_am_pm': selected_am_pm,
    }

    return render(request, 'cal/update_schedule.html', {'context': context})