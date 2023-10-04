"""olx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from olx_website import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from olx_website.forms import LogginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.test),
    path('', views.homepage, name='home-page'),
    path('item/<pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('user/create', views.UserCreateView.as_view(), name='create-user'),
    path('user_login/', views.CustomLoginView.as_view(), name='login'),
    path('add_item/', views.item_create_view, name='add-item'),
    path('delete/<pk>', views.DeleteItem, name='delete-item'),
    path('edit/<pk>', views.EditItemView.as_view(), name='update-item'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('user/logout', views.custom_logout, name='user-logout'),
    path('sport/', views.sport_category, name='sport-category'),
    path('electronics/', views.electronics_category, name='electronics-category'),
    path('clothes/', views.clothes_category, name='clothes-category'),
    path('browse/', views.browse, name='browse'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('rooms/create/<int:pk>/', views.new_room, name='create_room'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
