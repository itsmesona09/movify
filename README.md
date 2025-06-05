**MOVIFY**

Movify is a Python-based tool that allows you to migrate playlists from Apple Music to Spotify. Apple Music exports playlists in `.xml` format (used by iTunes). 
<br>It reads the `.xml` file, extracts song names and artists, searches for the tracks on Spotify using the Spotify API, and creates a new playlist on your Spotify account with the matching tracks.

<br>

**WHY DID I FIND THIS USEFUL?**

Apple Music is a paid service, and over time I’ve built up a ton of playlists there — like, seriously, it’s a whole music library! But switching over to Spotify, which I wanted to do because it’s free (or at least cheaper), meant I’d have to recreate every playlist by hand. Who has the patience for that?
<br>That’s why I made Movify. It’s a simple way to move all your playlists from Apple Music to Spotify without doing the boring copy-paste work. It just saves you so much time and hassle.
<br>Honestly, it’s also about not wanting to pay for two music subscriptions at once. Why spend extra money when you can get all your music in one place? Movify helps you keep your playlists, your sanity, and your wallet happy.

<br>

**HOW TO RUN THIS?**

1. Clone the repository and navigate into the project folder:
```bash
git clone [https://github.com/your-username/movify.git](https://github.com/your-username/movify.git)
cd movify
```
<br>

2. Set up your Python environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
<br>

3. Create a `.env` file in the root directory with your Spotify credentials:
```bash
SPOTIPY\_CLIENT\_ID=your\_spotify\_client\_id
SPOTIPY\_CLIENT\_SECRET=your\_spotify\_client\_secret
SPOTIPY\_REDIRECT\_URI=[http://localhost:8888/callback](http://localhost:8888/callback)
```
<br>

4. Export playlists from Apple Music:
In the Music app, go to File → Library → Export Playlist and save the file as `.xml`.
<br>

5. Move all `.xml` files into a folder called `playlists/`.
<br>

6. Run the script:
```bash
python main.py playlists/your\_playlist.xml
```
The playlist name will be automatically extracted from the XML file.

<br>

**FUTURE ENHANCEMENTS**
1. Create a web interface for uploading XML files
2. Support batch migration of multiple playlists
3. Enable exporting from other music platforms like YouTube Music or Amazon Music
4. Optionally keep track of playlists already migrated to avoid duplicates
