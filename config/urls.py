from django.contrib import admin
from django.urls import include, path
from timekeeping import views as time_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', time_views.dashboard, name='home'),
    path('timekeeping/', include('timekeeping.urls')),
    path('accounts/', include('accounts.urls')),
    path('holidays/', include('holidays.urls')),
]
