import plistlib

def parse_tracks_from_xml(xml_file):
    with open(xml_file, 'rb') as f:
        plist = plistlib.load(f)

    tracks_dict = plist.get('Tracks', {})
    tracks = []

    for track_id, track_info in tracks_dict.items():
        name = track_info.get('Name')
        artist = track_info.get('Artist')
        if name and artist:
            tracks.append({'name': name, 'artist': artist})
    return tracks

def parse_playlist_name_from_xml(xml_file):
    with open(xml_file, 'rb') as f:
        plist = plistlib.load(f)
    playlists = plist.get('Playlists', [])
    if playlists and 'Name' in playlists[0]:
        return playlists[0]['Name']
    return None