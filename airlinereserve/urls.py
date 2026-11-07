"""
URL configuration for airlinereserve project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('booking/<int:flight_id>/', views.booking, name='booking'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('logout/', views.logout_view, name='logout'),
    path('mybookings/', views.my_bookings, name='my_bookings'),
    path("cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path("profile/", views.profile, name="profile"),
    path("flight-status/<int:flight_id>/", views.flight_status, name="flight_status"),
    path("download-ticket/", views.download_ticket, name="download_ticket"),
    path("payment/<int:flight_id>/", views.payment, name="payment"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)