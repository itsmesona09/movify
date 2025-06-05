from spotify_client import create_playlist, create_spotify_client, get_spotify_uri, add_tracks_to_playlist
from parse_utils import parse_playlist_name_from_xml, parse_tracks_from_xml

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

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        sys.exit(1)

    xml_file = sys.argv[1]
    if len(sys.argv) > 2:
        playlist_name = sys.argv[2]
    else:
        playlist_name = parse_playlist_name_from_xml(xml_file)
    print(f"WELCOME TO MOVIFY!")
    print(f"Processing playlist: {playlist_name or 'Unnamed'}")
    migrate_playlist(xml_file, playlist_name)