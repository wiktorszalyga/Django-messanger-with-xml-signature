"""xmlSign URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.views.generic.base import TemplateView
from users.views import user_registretion_view, user_message_view, user_incoming_message_view, user_dynamic_incoming_message_view, user_incoming_message_file_view, user_incoming_message_verify,  user_settings

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('sign/', user_registretion_view, name='signup'),
    path('users/', include('django.contrib.auth.urls')),
    path('message/',user_message_view, name='message'),
    path('incoming/', user_incoming_message_view, name='incoming'),
    path('incoming/<int:id>/', user_dynamic_incoming_message_view, name='incoming_detail'),
    path('incoming/<int:id>/file/',  user_incoming_message_file_view, name='download'),
    path('incoming/<int:id>', user_incoming_message_verify, name='verify'),
    path('settings/', user_settings, name='settings'),
    path('incoming/<int:id>/verify/', user_incoming_message_verify, name='verify'),
]
