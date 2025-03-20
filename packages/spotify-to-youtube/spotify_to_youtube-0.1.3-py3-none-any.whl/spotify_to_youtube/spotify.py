import os
import re 

import spotipy
from spotipy.oauth2 import SpotifyOAuth


"""
client_id="98080bdb6392481d8126180b5902e8ba", 
client_secret="af09bef4fc094bf09b2b40490beaef38", 
"http://localhost:8000"
"""
SCOPE = "user-library-read playlist-read-private playlist-read-collaborative"

def is_song_in_playlist(playlist, name):
    for song in playlist:
        if name in song:
            return True
    return False


class Spotify_To_Youtube():
    def __init__(self, client_id, client_secret, redirect_uri):
        auth_manager = SpotifyOAuth(client_id=client_id, 
                                    client_secret=client_secret, 
                                    redirect_uri=redirect_uri,
                                    scope=SCOPE)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    # TODO: add create playlist feature
    def add_all_spotify_playlists(self, driver):
        playlists = self.sp.current_user_playlists(limit=50)
        while playlists:
            # Get all current playlists
            for playlist in playlists["items"]:
                playlist_name = playlist["name"]
                playlist_id = re.search(r"https://api.spotify.com/v1/playlists/(.+?)/tracks", playlist["tracks"]["href"])
                songs_in_playlist = driver.get_all_songs_in_playlist(f"Spotify-{playlist_name}") # TODO: might want to remove

                res_playlist = self.sp.playlist_tracks(playlist_id=playlist_id.group(1), limit=100)

                while res_playlist:
                    # Add all current tracks
                    for item in res_playlist["items"]:
                        # Omit song if already in playlist 
                        # TODO: might want to delete
                        if (is_song_in_playlist(songs_in_playlist, item['track']['name'])):
                            print(f"Found {item['track']['name']}")
                            continue

                        driver.create_playlist_search_and_add_video_to_playlist(item["track"]["name"], 
                                                                                item["track"]["artists"][0]["name"], 
                                                                                f"Spotify-{playlist_name}")
                        print(f"Added: {item['track']['name']} by {item['track']['artists'][0]['name']}")
                    # Go to next 100 tracks
                    if res_playlist["next"]:
                        res_playlist = self.sp.next(res_playlist)
                    else:
                        res_playlist = None
            
            # Get next 50 playlists
            if playlists["next"]:
                playlists = self.sp.next(playlists)
            else:
                playlists = None
    
    def add_spotify_playlist(self, driver, sp_playlist, yt_playlist=None):
        playlists = self.sp.current_user_playlists(limit=50)
        while playlists:
            # Get all current playlists
            for playlist in playlists["items"]:
                playlist_name = playlist["name"].strip()
                if playlist_name != sp_playlist:
                    continue

                songs_in_playlist = driver.get_all_songs_in_playlist(yt_playlist if yt_playlist else f"Spotify-{playlist_name}") # TODO: might want to remove

                playlist_id = re.search(r"https://api.spotify.com/v1/playlists/(.+?)/tracks", playlist["tracks"]["href"])
                res_playlist = self.sp.playlist_tracks(playlist_id=playlist_id.group(1), limit=100)

                while res_playlist:
                    # Add all current tracks
                    for item in res_playlist["items"]:
                        if (is_song_in_playlist(songs_in_playlist, item['track']['name'])):
                            continue

                        driver.create_playlist_search_and_add_video_to_playlist(item["track"]["name"], 
                                                                                item["track"]["artists"][0]["name"], 
                                                                                yt_playlist if yt_playlist else f"Spotify-{playlist_name}")
                        print(f"Successfully Added: {item['track']['name']}")
                    # Go to next 100 tracks
                    if res_playlist["next"]:
                        res_playlist = self.sp.next(res_playlist)
                    else:
                        res_playlist = None
                return
            
            # Get next 50 playlists
            if playlists["next"]:
                playlists = self.sp.next(playlists)
            else:
                playlists = None


    def add_spotify_liked(self, driver):
        liked = self.sp.current_user_saved_tracks(limit=20)
        while liked:
            for item in liked["items"]:
                driver.create_playlist_search_and_add_video_to_playlist(item["track"]["name"], 
                                                                        item["track"]["artists"][0]["name"], 
                                                                        f"Spotify-Liked")
                print(f"Added: {item['track']['name']}")
            # Go to next 20 tracks
            if liked["next"]:
                liked = self.sp.next(liked)
            else:
                liked = None

    # TODO: implement
    def add_song_to_yt_playlist(self, title, artist, yt_playlist):
        
        pass