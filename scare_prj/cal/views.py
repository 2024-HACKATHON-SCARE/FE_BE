from django.shortcuts import render
from datetime import datetime, timedelta, date
import calendar

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
                    month_days[i][j] = (prev_month_days - week.count(0) + 1, 'other-month')
                elif i == len(month_days) - 1:  # 마지막 주
                    month_days[i][j] = (box, 'other-month')
                    box += 1
            else:
                month_days[i][j] = (day, 'current-month')

    # 한국어 요일과 월을 설정
    weekdays = ["일", "월", "화", "수", "목", "금", "토"]
    
    context = {
        'year': year,
        'month': month,
        'cal_rows': month_days,
        'weekdays': weekdays,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    }

    return render(request, 'cal/home.html', context)

def home2(request, year, month, day):
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
    }

    return render(request, 'cal/home2.html', context)