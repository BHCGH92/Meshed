from django.shortcuts import render


def dashboard(request):
    return render(request, 'timekeeping/dashboard.html')


def timesheet(request):
    return render(request, 'placeholder.html', {'page_name': 'Timesheet'})


def export_timesheet(request):
    return render(request, 'placeholder.html', {'page_name': 'Export Timesheet'})


def audit_log(request):
    return render(request, 'placeholder.html', {'page_name': 'Audit Log'})
