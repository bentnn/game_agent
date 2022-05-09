from django.urls import path, include
from . import views
from course import urls

urlpatterns = [
    path('course/', include('course.urls')),
    path('home', views.home, name='home'),
    path('post/<int:id>', views.post_view, name='post'),
    path('', views.about_us, name='about_us'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('check_in', views.check_in_view, name='check_in'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/<str:username>/inventory', views.inventory, name='inventory'),
    path('search_user', views.search_user, name='search_user'),
    path('set_item/<int:id>', views.set_item, name='set_item'),
    path('game_shop', views.game_shop, name='game_shop'),
    path('game_shop/<int:id>/buy', views.buy_item, name='buy_item'),
    path('action/<str:username>/<str:action>', views.users_action, name='users_action'),
    path('settings', views.change_profile, name='change_profile'),
    path('settings/change_password', views.change_password, name='change_password'),

    path("password_reset", views.password_reset_request, name="password_reset"),
]

handler404 = "main.views.error_404"