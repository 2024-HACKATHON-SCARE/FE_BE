from django.shortcuts import render
from datetime import datetime, timedelta
import calendar
# test
# from calendar import HTMLCalendar
# 캘린더랑 데이트타임 필요


def home(request):
    today = datetime.today()
    month = today.month
    year = today.year
    today_day = today.day

    # 달력의 첫 요일을 일요일로 설정
    calendar.setfirstweekday(calendar.SUNDAY)

    # 현재 달의 첫날과 마지막 날
    first_day_of_month = datetime(year, month, 1)
    last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # 이전 달과 다음 달의 날짜 계산
    start_date = first_day_of_month - timedelta(days=first_day_of_month.weekday() + 1)  # 일요일 이전으로 설정
    last_day_of_week = last_day_of_month + timedelta(days=(5 - last_day_of_month.weekday() + 7) % 7) # 다음 월의 마지막 토요일까지
    end_date = last_day_of_week

    # 달력 데이터 생성
    cal_data = []
    current_date = start_date
    while current_date <= end_date:
        week_data = []
        for _ in range(7):
            if current_date.month == month:
                # 현재 달의 날짜
                day = current_date.day
                day_class = 'current-month'
            else:
                # 이전 또는 다음 달의 날짜
                day = current_date.day
                day_class = 'other-month'
            week_data.append((day, day_class))
            current_date += timedelta(days=1)
        cal_data.append(week_data)

    context = {
        'month': month,
        'year': year,
        'today_day': today_day,
        'cal_data': cal_data,
    }

    return render(request, 'cal/home.html', context)


# from .calendars import CustomHTMLCalendar  # 커스터마이즈된 달력 클래스를 import
from datetime import date

def home2(request, year, month):
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
    }
    
    return render(request, 'cal/home2.html', context)