from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_song, name='search_song'),
    path('song_details/<str:song_id>/', views.song_details, name='song_details'),
]
