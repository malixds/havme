from django.urls import path
from . import views

urlpatterns = [
    # path('me', views.me, name='me'),
    path('settings', views.settings, name='settings'),
    # path('upload', views.upload, name='upload'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('@<str:pk>', views.profile, name='profile'),
    path('search', views.search, name='search'),
    path('', views.start, name=''),
]