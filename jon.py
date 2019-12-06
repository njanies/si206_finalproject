import sys
import spotipy
import spotipy.util as util

util.prompt_for_user_token("jon.m.rosenblum",client_id='y3555bee94ce244a4b4ce2e2f99b45938',client_secret='3132de5ff9584f6a8eea601dac4a7412',redirect_uri='http://localhost/')
birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify()

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])

username = "jon.m.rosenblum"


scope = 'user-library-read'
name = "Drake"
spotify = spotipy.Spotify()
results = spotify.search(q='artist:' + name, type='artist')
print(results)

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
else:
    print("Can't get token for", username)