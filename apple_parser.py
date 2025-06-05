from lxml import etree
import requests

def parse_apple_playlist(xml_path, playlist_name=None):
    with open(xml_path, 'rb') as f:
        tree = etree.parse(f)

    # Navigate to the root <dict>
    root_dict = tree.xpath('/plist/dict')[0]

    # Step 1: Build a map of all tracks by Track ID
    tracks = {}
    track_dict = root_dict.xpath("key[.='Tracks']/following-sibling::dict[1]")[0]
    for i in range(0, len(track_dict), 2):
        track_id = track_dict[i].text
        track_info = track_dict[i+1]
        name = track_info.xpath("string[key='Name']/following-sibling::*[1]")
        artist = track_info.xpath("string[key='Artist']/following-sibling::*[1]")

        if name and artist:
            tracks[int(track_id)] = {
                'name': name,
                'artist': artist
            }

    # Step 2: Locate the playlist
    playlist_array = root_dict.xpath("key[.='Playlists']/following-sibling::array[1]")[0]
    for plist in playlist_array.xpath('dict'):
        name = plist.xpath("string[key='Name']/following-sibling::*[1]")
        if not name or (playlist_name and name != playlist_name):
            continue

        playlist_items = plist.xpath("key[.='Playlist Items']/following-sibling::array[1]/dict")
        track_list = []
        for item in playlist_items:
            track_id = item.xpath("number[key='Track ID']/following-sibling::*[1]")
            if track_id:
                tid = int(track_id)
                if tid in tracks:
                    track_list.append(tracks[tid])
        return track_list

    return []  # Playlist not found or empty

def parse_apple_music_url(playlist_url):
    # Extract playlist ID from URL
    playlist_id = playlist_url.rstrip('/').split('/')[-1]
    
    # Apple Music API endpoint to fetch playlist details (requires a developer token)
    # For demo, we'll use the public iTunes Search API (limited)
    
    # Construct API URL (note: iTunes API has limited playlist support)
    # Real Apple Music API requires auth token (MusicKit)
    
    api_url = f"https://itunes.apple.com/lookup?id={playlist_id}&entity=song"
    
    response = requests.get(api_url)
    if response.status_code != 200:
        print("Failed to fetch playlist data from Apple Music API")
        return []
    
    data = response.json()
    tracks = []
    for item in data.get('results', []):
        if item.get('wrapperType') == 'track':
            tracks.append({
                'name': item.get('trackName'),
                'artist': item.get('artistName')
            })
    return tracks