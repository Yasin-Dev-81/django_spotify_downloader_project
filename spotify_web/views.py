from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from config.settings import BASE_DIR

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotdl import Spotdl

from os import listdir

from . import tasks

spotify_secret_data = {'CLIENT_ID': 'c5739c2b9f3949d7ada667c549671810', 'CLIENT_SECRET': '3ec11f1a57e44e78bb44e90ac4fb2f21'}


# finished
@csrf_exempt
def search_view(request, selected_search_type):
    if selected_search_type in ['track', 'artist', 'album', 'playlist']:
        search_types = ['track', 'artist', 'album', 'playlist']
        search_types.remove(selected_search_type)
        if request.method == "POST" or 'search_button' in request.POST:
            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_secret_data["CLIENT_ID"], client_secret=spotify_secret_data["CLIENT_SECRET"]))
            search_key = request.POST.get("search_input")
            print('search key:', search_key)
            results = sp.search(q=search_key, limit=20, type=selected_search_type)
            # print(results)
            return render(
                request,
                'spotify_web/search.html',
                context={
                    'search_types': search_types,
                    'results_list': enumerate(results[f'{selected_search_type}s']['items']),
                    'search_key': search_key,
                    'selected_search_type': selected_search_type
                }
            )
        else:
            return render(request, 'spotify_web/search.html', context={'search_types': search_types, 'selected_search_type': selected_search_type})
    else:
        return HttpResponse("error in search type")


# finished
def detail_view(requests, search_type, search_id):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_secret_data["CLIENT_ID"],
                                                               client_secret=spotify_secret_data["CLIENT_SECRET"]))
    uri = 'spotify:%s:%s' % (search_type, search_id)
    if search_type == 'track':
        tracks_list = ((0, sp.track(uri)), )
        title_data = sp.artist(tracks_list[0][1]['artists'][0]['uri'])

    elif search_type == 'artist':
         tracks_list = enumerate(sp.artist_top_tracks(uri)['tracks'])
         title_data = sp.artist(uri)

    elif search_type == 'album':
        tracks_list = enumerate(sp.album_tracks(uri)['items'])
        title_data = sp.album(uri)

    elif search_type == 'playlist':
        play_list = sp.playlist(uri)
        tracks_list = enumerate([i.get('track') for i in play_list['tracks']['items']])
        # print(play_list['tracks']['items'][0])
        title_data = play_list
        # print(title_data)
    return render(requests, 'spotify_web/detail.html', context={'tracks_list': tracks_list, 'selected_search_type': search_type, 'title_data': title_data})


# finished
def song_download_view(request, song_id):
    # print(listdir(BASE_DIR.joinpath('spotify_downloaded_file')))
    if ('%s.mp3' % song_id) in listdir(BASE_DIR.joinpath('spotify_downloaded_file')):
        with open(BASE_DIR.joinpath('spotify_downloaded_file', f'{song_id}.mp3'), 'rb') as song:
            response = HttpResponse(song, content_type='audio/mpeg')
            # response['Content-Disposition'] = "attachment; filename=%s - %s.mp3" % (song.artist, song.title)
            return response
    else:
        tasks.DownloadSong(song_id, spotify_secret_data).start()
        return render(request, 'spotify_web/download.html', context={'track_id': song_id})
