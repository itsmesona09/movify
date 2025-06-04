import tkinter as tk
from tkinter import filedialog, messagebox
from spotify_client import create_playlist, get_spotify_uri, add_tracks_to_playlist
import plistlib
import os

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

def migrate_playlist(xml_file, playlist_name=None):
    if playlist_name is None:
        playlist_name = os.path.splitext(os.path.basename(xml_file))[0]

    tracks = parse_tracks_from_xml(xml_file)
    spotify_uris = []

    for t in tracks:
        uri = get_spotify_uri(t['name'], t['artist'])
        if uri:
            spotify_uris.append(uri)

    print(f"✅ Found {len(spotify_uris)} tracks on Spotify")

    playlist_id = create_playlist(playlist_name)
    add_tracks_to_playlist(playlist_id, spotify_uris)
    messagebox.showinfo("Success", f"Playlist '{playlist_name}' created with {len(spotify_uris)} tracks!")

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def start_migration():
    xml_file = entry_file_path.get().strip()
    if not xml_file:
        messagebox.showwarning("Error", "Please select or enter the path to an XML file.")
        return
    try:
        migrate_playlist(xml_file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to migrate playlist:\n{e}")

# Create main window
root = tk.Tk()
root.title("Movify - Spotify Playlist Sync")

# Entry for XML file path
tk.Label(root, text="Select XML file:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
entry_file_path = tk.Entry(root, width=50)
entry_file_path.grid(row=0, column=1, padx=10)

# Browse button
btn_browse = tk.Button(root, text="Browse", command=select_file)
btn_browse.grid(row=0, column=2, padx=10)

# Sync button
btn_sync = tk.Button(root, text="Sync Playlist to Spotify", command=start_migration)
btn_sync.grid(row=1, column=1, pady=20)

root.mainloop()
