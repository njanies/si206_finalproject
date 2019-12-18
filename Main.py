import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json
import random
import sqlite3
import os.path
import requests
from musixmatch import Musixmatch
from Utils import jointables
from Utils import countsame
from Utils import jointables2
from Utils import barchart_musixmatch
from Utils import barchart_spotify

cid ='bc4107086c834d10a1fa8616f1f4230a' 
secret = 'ca5d5a3a7ec741bf9dd9e045117b2730' 
username = 'njchoco'
playlist_id = '4JHy5WbZrBrOYUJ6CzOtd5'
track_ids = '11dFghVXANMlKmJXsNCbNl'

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

for x in range(4): 
    seed_tracks = random.sample(id_list, 5)
    list_recommendations = sp.recommendations(seed_tracks = seed_tracks, limit = 5)
    track_recommendations = []
    genres = []
    artist_names_recommendations = []
    popularity = []
    for track in list_recommendations['tracks']:
        track_recommendations.append((track['name']))
        popularity.append((track['popularity']))
        artist_info = track['artists']
        tmp = sp.artist(artist_info[0]['id'])['genres']
        if len(tmp) == 0:
            genres.append('')
        else:
            genres.append(tmp[0])
        artist_names_recommendations.append(artist_info[0]['name'])

    #write to sql file 
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "206.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # create the table 
    c.execute('CREATE TABLE IF NOT EXISTS Spotify_Genres (artist_names TEXT, genres TEXT)')
    data1 = list(zip(artist_names_recommendations, genres))
    #make it so no duplicates 
    for i in data1:
        if (c.execute('SELECT artist_names FROM Spotify_Genres WHERE artist_names = ?', (i[0],)).fetchone() == None):
            c.execute('INSERT INTO Spotify_Genres(artist_names, genres) VALUES (?,?)', (i[0], i[1]))
    data2 = list(zip(track_recommendations, popularity))
    c.execute('CREATE TABLE IF NOT EXISTS Spotify_PopScores (songs TEXT, popularity TEXT)')
    for i in data2:
        if (c.execute('SELECT songs FROM Spotify_PopScores WHERE songs = ?', (i[0],)).fetchone() == None):
            c.execute('INSERT INTO Spotify_PopScores(songs, popularity) VALUES (?,?)', (i[0], i[1]))
    conn.commit()

###########################################################################################

musixmatch = Musixmatch('a8910b91fed84a97ec71b4023e102863')

temp_tracks_list = sp.tracks(seed_tracks)
artist_names_original = []
track_names_original = []
for track in temp_tracks_list['tracks']:
    artist_names_original.append(track['artists'][0]['name'])
    track_names_original.append(track['name'])

artist_id_musixmatch = []
for i in range(5):
    temp = musixmatch.matcher_track_get(q_track = track_names_original[i], q_artist = artist_names_original[i], _format='json' )
    if temp['message']['body'] == '':
        pass
    else:
        artist_id_musixmatch.append(temp['message']['body']['track']['artist_id'])

new_artists_id = []
for id in artist_id_musixmatch:
    new_artists = musixmatch.artist_related_get(artist_id = id, page = 1, page_size = 4)
    for temp_artist in new_artists['message']['body']['artist_list']:
        new_artists_id.append(temp_artist['artist']['artist_id'])

new_song_tuples = []
new_artists_names = []
new_artists_genres = []
for id in new_artists_id:
    album_info = musixmatch.artist_albums_get(id, page = 1, page_size = 10, g_album_name = 1, s_release_date= 'asc')
    try:
        temp_album = random.sample(album_info['message']['body']['album_list'], 1)
        if temp_album[0]['album']['album_id']:
            temp_songs = musixmatch.album_tracks_get(album_id=temp_album[0]['album']['album_id'], page = 1, page_size = 20, album_mbid=temp_album[0]['album']['album_mbid'] )
        if len(temp_songs['message']['body']['track_list']) == 0:
            pass
        else:
            new_song = random.sample(temp_songs['message']['body']['track_list'], 1)
            new_song = new_song[0]
            new_song_name = new_song['track']['track_name']
            new_song_rating = new_song['track']['track_rating']
            new_artists_names.append(new_song['track']['artist_name'])
            for album in album_info['message']['body']['album_list']:
                if album['album']['primary_genres']['music_genre_list'] != []:
                    new_artists_genres.append(album['album']['primary_genres']['music_genre_list'][0]['music_genre']['music_genre_name'].lower())
                    break
                else:
                    continue
            if new_artists_genres == []:
                new_artists_genres.append("NO GENRE GIVEN")
    except:
        print('\n')
        print('No albumn info')
        print('\n')
        continue
    new_song_tuples.append((new_song_name, new_song_rating))
print(new_song_tuples)
print(new_artists_names)
print(new_artists_genres)

#write to sql file 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "206.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()
# create the table 
c.execute('CREATE TABLE IF NOT EXISTS Musixmatch_Genres (artist_names TEXT, genres TEXT)')
musixmatch_data1 = list(zip(new_artists_names, new_artists_genres))
#make it so no duplicates 
for i in musixmatch_data1:
    if (c.execute('SELECT artist_names FROM Musixmatch_Genres WHERE artist_names = ?', (i[0],)).fetchone() == None):
        c.execute('INSERT INTO Musixmatch_Genres(artist_names, genres) VALUES (?,?)', (i[0], i[1]))
musixmatch_data2 = new_song_tuples
c.execute('CREATE TABLE IF NOT EXISTS Musixmatch_PopScores (songs TEXT, popularity TEXT)')
for i in musixmatch_data2:
    if (c.execute('SELECT songs FROM Musixmatch_PopScores WHERE songs = ?', (i[0],)).fetchone() == None):
        c.execute('INSERT INTO Musixmatch_PopScores(songs, popularity) VALUES (?,?)', (i[0], i[1]))
conn.commit()
c.close()






jointables("206.db")
jointables2("206.db")
same_count, different_count = countsame("206.db")
barchart_musixmatch("206.db")
barchart_spotify("206.db")
print(same_count, different_count)









        