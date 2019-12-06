import spotipy
import spotipy.util as util


util.prompt_for_user_token("jjon.m.rosenblum",scope,client_id='y3555bee94ce244a4b4ce2e2f99b45938',client_secret='3132de5ff9584f6a8eea601dac4a7412',redirect_uri='http://localhost/?code=')
name = "Drake"
spotify = spotipy.Spotify()
results = spotify.search(q='artist:' + name, type='artist')
print(results)