from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login', auth_views.login, name='login'),
    path('logout', auth_views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('', views.index, name='index'),
    #path('dashboard/<string:country>/detail', views.detail, name='detail'),
    #path('dashboard/<string:country>/issues', views.issues, name='issues'),
    #path('dashboard/reply/<string:tweet_id>', views.reply, name='reply'),
    path('dashboard', views.dashboard, name='index')
]