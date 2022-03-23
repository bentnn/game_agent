from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about_us, name='about_us'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('check_in', views.check_in_view, name='check_in'),
    path('profile/<str:username>', views.profile, name='profile'),
]

handler404 = "main.views.error_404"
