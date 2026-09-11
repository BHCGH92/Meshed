from django.shortcuts import render


def company_info(request):
    return render(request, 'placeholder.html', {'page_name': 'Company Info'})


def admin_user_list(request):
    return render(request, 'placeholder.html', {'page_name': 'User Management'})


def profile(request):
    return render(request, 'accounts/profile.html')
