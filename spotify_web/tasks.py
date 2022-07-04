import threading
from config.settings import BASE_DIR

from spotdl import Spotdl


class DownloadSong(threading.Thread):
    def __init__(self, track_id: str, spotify_secret_data: dict):
        self.track_id = track_id
        self.spotify_secret_data = spotify_secret_data
        threading.Thread.__init__(self)

    def run(self):
        song_path = BASE_DIR.joinpath('spotify_downloaded_file', f'{self.track_id}.mp3')
        spotdl = Spotdl(client_id=self.spotify_secret_data["CLIENT_ID"], client_secret=self.spotify_secret_data["CLIENT_SECRET"], save_file=song_path)
        songs = spotdl.search(['https://open.spotify.com/track/%s' % self.track_id])
        # print(songs)
        song, path = spotdl.download(songs[0])
        print('---- download finished:)')
