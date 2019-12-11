import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json
import random
import sqlite3
import os.path

cid ='bc4107086c834d10a1fa8616f1f4230a' 
secret = 'ca5d5a3a7ec741bf9dd9e045117b2730' 
username = 'njchoco'
playlist_id = '4JHy5WbZrBrOYUJ6CzOtd5'
track_ids = '11dFghVXANMlKmJXsNCbNl'


#for avaliable scopes see https://developer.spotify.com/web-api/using-scopes/
scope = 'user-library-read playlist-modify-public playlist-read-private'
redirect_uri = 'https://developer.spotify.com/dashboard/applications/bc4107086c834d10a1fa8616f1f4230a'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
token = util.prompt_for_user_token(username, scope, cid, secret, redirect_uri)


sp = spotipy.Spotify(auth=token)
results = sp.user_playlist_tracks(username, playlist_id)

id_list = []
for song in results['items']:
    id_list.append(song['track']['id'])

random.seed(1234)
list_recommendations = sp.recommendations(seed_tracks = random.sample(id_list, 5), limit = 20)
track_recommendations = []
genres = []
artist_names = []
for track in list_recommendations['tracks']:
    track_recommendations.append((track['name']))
    for artist in track['artists']:
        tmp = sp.artist(artist['id'])['genres']
        if len(tmp) == 0:
            genres.append('')
        else:
            genres.append(sp.artist(artist['id'])['genres'][0])
        artist_names.append(artist['name'])


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "206.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()
data = list(zip(artist_names, genres))
c.executemany('INSERT INTO Spotify_Artists VALUES (?,?)', data)
conn.commit()





