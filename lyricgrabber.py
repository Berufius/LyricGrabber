import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lyricsgenius
from time import sleep
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, USER, GENIUS_TOKEN


def main():
    # Scope = currently playing track
    scope = "user-read-currently-playing"
    # Create spotify object
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,scope=scope,username=USER))
    # Set track name to nothing
    track = ""
    while True:
        # Receive Spotify response
        results = sp.current_user_playing_track()
        if results != None:
            # Check if same song as previous iteration still plays
            if not track == results['item']['name']:
                artist = results['item']['artists'][0]['name']
                album = results['item']['album']['name']
                track = results['item']['name']
                # Print lyrics
                print_lyrics(artist, track, album)
        else:
            # Nothing is playing, quitting script
            print("Nothing is playing, exit script...")
            return
        sleep(10)


def print_lyrics(artist, track, album):
    """ Searches song lyrics in genius db and prints them

    Args:
        artist (string): artist name
        track (string): track name
        album (string): album name
    """
    # Genius object and properties
    genius = lyricsgenius.Genius(GENIUS_TOKEN)
    genius.skip_non_songs = True
    genius.excluded_terms = ["(Remix)", "(Live)", "(Instrumental)"]
    # Request genius object
    song = genius.search_song(title=track, artist=artist)
    # Check if genius object corresponds with spotify object parameters
    if (song != None and str(song.artist).lower() == artist.lower()):
        # Print lyrics and song parameters
        print(f"\nArtist: {artist}\nAlbum: {album}\nTrack name: {track}\n{song.lyrics}\n")
    else:
        print(f"There are no lyrics available for:\n{artist} - {track}")
    return


if __name__ == "__main__":
    main()



