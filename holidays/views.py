from django.shortcuts import render


def holiday_calendar(request):
    return render(request, 'placeholder.html', {'page_name': 'Calendar'})


def my_requests(request):
    return render(request, 'placeholder.html', {'page_name': 'My Holidays'})


def pending_requests(request):
    return render(request, 'placeholder.html', {'page_name': 'Pending Requests'})


def company_holidays(request):
    return render(request, 'placeholder.html', {'page_name': 'Company Holidays'})
