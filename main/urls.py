from django.urls import path, include
from . import views
from course import urls

urlpatterns = [
    path('course/', include('course.urls')),
    path('home', views.home, name='home'),
    path('', views.about_us, name='about_us'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('check_in', views.check_in_view, name='check_in'),
    # path('reset_password', views.reset_password, name='reset_password'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/<str:username>/inventory', views.inventory, name='inventory'),
    path('set_item/<int:id>', views.set_item, name='set_item'),
    path('game_shop', views.game_shop, name='game_shop'),
    path('game_shop/<int:id>/buy', views.buy_item, name='buy_item'),
    path('action/<str:username>/<str:action>', views.users_action, name='users_action'),
    path('change_profile', views.change_profile, name='change_profile'),
    path('change_profile/password', views.change_password, name='change_password'),
]

handler404 = "main.views.error_404"

