from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login', auth_views.login, name='login'),
    path('logout', auth_views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('', views.index, name='index'),
    path('tweets', views.tweets, name='tweets'),
    path('dashboard/<country>/statuses', views.statuses, name='statuses'),
    path('dashboard/<country>/feedback', views.feedbacks, name='feedbacks'),
    path('dashboard/<country>/promotions', views.promotions, name='promotions'),
    path('dashboard/<country>/issues', views.issues, name='issues'),
    #path('dashboard/reply/<string:tweet_id>', views.reply, name='reply'),
    path('dashboard', views.dashboard, name='dashboard')
]