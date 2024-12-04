from django.contrib import admin
from django.urls import path, include
from filmy.views import HomeScreen
from filmy.views import HomeScreenAPI
from mostrarinfo.views import show_movie_info
from mostrarinfo.views import show_movie_info_api
from mostrarinfo.views import add_to_watchlist_api
from autenticacao.views import *
from userprofile.views import watchlist, remove_from_watchlist

urlpatterns = [
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name="Login"),
    path('api/login/', LoginMobile.as_view(), name='mobile_login'),  # Versão API para App Mobile
    path('api/logout/', LogoutMobile.as_view(), name='mobile_logout'),  # Versão API para App Mobile
    path('api/register/', RegisterMobile.as_view(), name='mobile_register'),  # Versão API para App Mobile
    path('filme/<int:movie_id>/', show_movie_info, name="show_movie_info"),
    path('api/filme/<int:movie_id>/', show_movie_info_api, name='show_movie_info_api'),  # Versão API para o App Mobile
    path('api/watchlist/add/', add_to_watchlist_api, name='add_to_watchlist_api'),  # Versão API para adicionar à watchlist
    path('', HomeScreen, name="HomeScreen"),
    path('api/home/', HomeScreenAPI, name='home_api'),  # Versão API para o App Mobile
    path('admin/', admin.site.urls),
    path('profile/', watchlist, name="Profile"),
    path('profile/remove/', remove_from_watchlist, name='RemoveFromWatchlist'),
    
]
