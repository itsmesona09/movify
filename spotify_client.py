import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-modify-public"
    ))
    return sp

def get_spotify_uri(sp, track_name, artist_name):
    query = f"{track_name} {artist_name}"
    result = sp.search(q=query, type="track", limit=1)
    tracks = result.get("tracks", {}).get("items", [])
    if tracks:
        return tracks[0]["uri"]
    return None

def create_playlist(sp, name):
    user_id = sp.me()["id"]
    playlist = sp.user_playlist_create(user_id, name)
    return playlist["id"]

def add_tracks_to_playlist(sp, playlist_id, uris):
    if not uris:
        print("⚠️ No Spotify URIs found. Skipping playlist creation.")
        return
    chunk_size = 100
    for i in range(0, len(uris), chunk_size):
        chunk = uris[i:i + chunk_size]
        sp.playlist_add_items(playlist_id, chunk)
