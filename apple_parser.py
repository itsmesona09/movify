from lxml import etree
import requests

def parse_apple_playlist(xml_path, playlist_name=None):
    with open(xml_path, 'rb') as f:
        tree = etree.parse(f)
    root_dict = tree.xpath('/plist/dict')[0]

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

    return []