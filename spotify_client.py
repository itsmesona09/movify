import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-modify-public"
))

def get_spotify_uri(track_name, artist_name):
    query = f'track:{track_name} artist:{artist_name}'
    print(f"🔍 Searching Spotify for: {query}")
    result = sp.search(q=query, type='track', limit=1)
    items = result.get('tracks', {}).get('items', [])
    if items:
        uri = items[0]['uri']
        print(f"✅ Found URI: {uri}")
        return uri
    print("❌ No track found")
    return None

def create_playlist(name):
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user=user_id, name=name)
    return playlist["id"]

def add_tracks_to_playlist(playlist_id, uris):
    if not uris:
        print("⚠️ No Spotify URIs found. Skipping playlist creation.")
        return
    chunk_size = 100

    for i in range(0, len(uris), chunk_size):
        chunk = uris[i:i + chunk_size]
        sp.playlist_add_items(playlist_id, chunk)