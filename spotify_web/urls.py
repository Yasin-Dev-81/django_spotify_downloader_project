from django.urls import path
from . import views

urlpatterns = [
    path('search/<str:selected_search_type>', views.search_view, name='spotify_search_url'),
    path('detail/<str:search_type>/<str:search_id>', views.detail_view, name='spotify_detail_url'),
    path('download/<str:song_id>/', views.song_download_view, name='spotify_download_url'),
]
