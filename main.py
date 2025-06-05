import os
import sys
from spotify_client import create_playlist, create_spotify_client, get_spotify_uri, add_tracks_to_playlist
from parse_utils import parse_tracks_from_xml

def migrate_playlist(xml_file, playlist_name):
    tracks = parse_tracks_from_xml(xml_file)
    sp = create_spotify_client()
    spotify_uris = []
    for t in tracks:
        uri = get_spotify_uri(sp, t['name'], t['artist'])
        if uri:
            spotify_uris.append(uri)
    print(f"Found {len(spotify_uris)} tracks on Spotify")
    playlist_id = create_playlist(sp, playlist_name)
    add_tracks_to_playlist(sp, playlist_id, spotify_uris)

PLAYLISTS_FOLDER = "playlists"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    filename = sys.argv[1]
    if not os.path.isabs(filename) and not os.path.exists(filename):
        xml_file = os.path.join(PLAYLISTS_FOLDER, filename)
    else:
        xml_file = filename
    playlist_name = sys.argv[2] if len(sys.argv) > 2 else None
    print(f"WELCOME TO MOVIFY!!!")
    if not playlist_name:
        base = os.path.basename(filename)
        playlist_name = os.path.splitext(base)[0]
    print(f"Processing playlist: {playlist_name}")
    migrate_playlist(xml_file, playlist_name)