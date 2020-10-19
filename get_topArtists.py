import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from operator import itemgetter

#Declare some vars we need
baseurl = "https://api.spotify.com/v1/"
cid = 'YOURCLIENTID' #create an api in the dev dashboard
secret = 'YOURCLIENTAPP' #create a secret for said app
grant_type = 'client_credentials'
your_scopes = ['user-top-read'] #this is the only scope we need for this purpose
body_params = {
'grant_type' : grant_type,
'scope' : your_scopes
}


os.environ['SPOTIPY_CLIENT_ID']= cid
os.environ['SPOTIPY_CLIENT_SECRET']= secret
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:8888/callback/' #IMPORTANT whitelist this callback URI in your app EXACTLY as it is written here

username = "YOURACCOUNTHERE" #you can use a prompt for this if you want
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
scope = 'user-top-read'
token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Cannot get a token for this user. Exiting.")
    exit()

genres = []
favorites = {
'short_term':[],
'medium_term':[],
'long_term':[]
}

terms = ['short_term','medium_term','long_term']

for t in terms:

    top = sp.current_user_top_artists(limit=50,offset=0,time_range=t)
    for r in top['items']:
        tmp = {'name':'','genres':[],'term':''}
        tmp['name'] = r['name']
        tmp['genres'] = r['genres']
        tmp['popularity'] = r['popularity']
        tmp['followers'] = r['followers']['total']
        tmp['term'] = t
        if tmp not in favorites[t]:
            favorites[t].append(tmp)

        for g in r['genres']:
            if not any(g in d.values() for d in genres):
                genres.append({'genre':g,'count':1})
            else:
                for item in genres:
                    if item['genre'] == g:
                        item['count']+=1

final = sorted(genres, key=itemgetter('count'))


with open('top_data.json', 'w', encoding='utf-8') as f:
    json.dump(favorites, f, ensure_ascii=False, indent=4)
