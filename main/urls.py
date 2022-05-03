from django.urls import path, include
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.about_us, name='about_us'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('check_in', views.check_in_view, name='check_in'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/<str:username>/<str:action>', views.profile, name='profile'),
    path('change_profile', views.change_profile, name='change_profile')
]

handler404 = "main.views.error_404"