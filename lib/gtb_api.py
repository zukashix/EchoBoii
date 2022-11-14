import base64
import json
import random
import requests
import sys

from fuzzysearch import find_near_matches
import lyricsgenius as lg

urlsDict = json.load(open('data/urls.json', 'r'))
keysDict = json.load(open('data/api_keys.json', 'r'))

lyricapis = lg.Genius(keysDict["Lyricgenius_API_KEY"], skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

# Client Keys
CLIENT_ID = keysDict["Spotify_Client_ID"]
CLIENT_SECRET = keysDict["Spotify_Client_Secret"]

# Spotify API URIs
SPOTIFY_TOKEN_URL = urlsDict["Spotify_Token_URL"]
SPOTIFY_API_BASE_URL = urlsDict["Spotify_API_URL"]
API_VERSION = keysDict["Spotify_API_Version"]
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

def __get_token():
    client_token = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode('UTF-8')).decode('ascii')
    headers = {"Authorization": "Basic {}".format(client_token)}
    payload = {"grant_type": "client_credentials"}
    token_request = requests.post(SPOTIFY_TOKEN_URL, data=payload, headers=headers)
    access_token = json.loads(token_request.text)["access_token"]
    return access_token


def __request_valid_song(access_token, genre=None):
    random_wildcards = ['%25a%25', 'a%25', '%25a',
                        '%25e%25', 'e%25', '%25e',
                        '%25i%25', 'i%25', '%25i',
                        '%25o%25', 'o%25', '%25o',
                        '%25u%25', 'u%25', '%25u']
    wildcard = random.choice(random_wildcards)
    
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    
    song = None
    for i in range(51):
        try:
            song_request = requests.get(
                '{}/search?q={}{}&type=track&offset={}'.format(
                    SPOTIFY_API_URL,
                    wildcard,
                    "%20genre:%22{}%22".format(genre.replace(" ", "%20")),
                    random.randint(0, 200)
                ),
                headers = authorization_header
            )
            song_info = random.choice(json.loads(song_request.text)['tracks']['items'])
            artist = song_info['artists'][0]['name']
            song = song_info['name']
            break
        except IndexError:
            continue
        
    if song is None:
        artist = "Rick Astley"
        song = "Never Gonna Give You Up"
        
    return (song, artist)


def return_song():
    args = sys.argv[1:]
    n_args = len(args)

    access_token = __get_token()
    
    try:
        with open('data/genres.json', 'r') as infile:
            valid_genres = json.load(infile)
    except FileNotFoundError:
        print("Couldn't find genres file!")

    if n_args == 0:
        selected_genre = random.choice(valid_genres)
    else:
        selected_genre = (" ".join(args)).lower()
    
    if selected_genre in valid_genres:
        result = __request_valid_song(access_token, genre=selected_genre)
        return result
    else:
        valid_genres_to_text = " ".join(valid_genres)
        try:
            closest_genre = find_near_matches(selected_genre, valid_genres_to_text,  max_l_dist=2)[0].matched
            result = __request_valid_song(access_token, genre=closest_genre)
            return result
        except IndexError:
            print("Genre not found")

def get_lyrics(song, artist):
    try:
        lyric = (lyricapis.search_song(song, artist)).lyrics
        larr = lyric.split('\n')
        return larr
    except:
        print(f"some exception at {song}")
