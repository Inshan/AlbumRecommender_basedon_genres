from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_band, name='search_band'),
    path('band_albums/<str:artist_id>/', views.band_albums, name='band_albums'),
    path('recommendations/<str:artist_id>/', views.recommendations, name='recommendations'),
]
