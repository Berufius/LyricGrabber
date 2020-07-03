import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lyricsgenius
from time import sleep
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, user, genius_token


# Scope = currently playing track
scope = "user-read-currently-playing"
# Create spotify object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,scope=scope,username=user))
# Genius object and properties
genius = lyricsgenius.Genius(genius_token)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)", "(Instrumental)"]
# Set track name to nothing
track_name = ""

while True:
    # Receive Spotify response
    results = sp.current_user_playing_track()
    if not results == None:
        # Different song as previous iteration still plays
        if not track_name == results['item']['name']:
            artist = results['item']['artists'][0]['name']
            album = results['item']['album']['name']
            track_name = results['item']['name']
            # print summary
            song = genius.search_song(title=track_name, artist=artist)
            # Check if genius return values correspond with spotipy
            if str(song.artist).lower() == artist.lower() and str(song.title).lower() == track_name.lower():
                print(f"\nArtist: {artist}")
                print(f"Album: {album}")
                print(f"Track name: {track_name}\n")
                print(song.lyrics)
                print()
            else:
                print(f"There are no lyrics available for\n{artist} - {track_name}")
    else:
        # Nothing is playing, quitting script
        print("Nothing is playing, exit script...")
        break
    sleep(10)

