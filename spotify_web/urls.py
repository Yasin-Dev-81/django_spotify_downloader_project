from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='spotify_search_url'),
    path('download/<str:type>/<str:id>', views.download, name='spotify_download_url'),
]
