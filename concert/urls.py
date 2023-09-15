"""
URL configuration for concert project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from dashboard.views import home , SignUpView,UserSignUpView, ArtistSignUpView, ConcertListView, \
             ConcertCreateView, ConcertUpdateView , ConcertDeleteView, UserConcertListView
from django.conf import settings
from django.conf.urls.static import static
from booking.views import concert_list, concert_details

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
	path('booking/', concert_list, name = 'booking'),
    path('booking/<booking_id>/',concert_details, name='concert_details'),
	path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/signup/user/', UserSignUpView.as_view(), name='user_signup'),
    path('accounts/signup/artist/', ArtistSignUpView.as_view(), name='artist_signup'),
    path('concert-list', ConcertListView.as_view(), name='concert_change_list'),
	path('concert-add', ConcertCreateView.as_view(), name='concert_add_form'),
	path('concert-update/<pk>', ConcertUpdateView.as_view(), name='concert_change_form'),
	path('concert-delete/<pk>', ConcertDeleteView.as_view(), name='concert_delete_confirm'),
	path('all-concert', UserConcertListView.as_view(), name='user_concert_list'),



]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #all values set in settings.py
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
