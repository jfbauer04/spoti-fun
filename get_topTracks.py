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
your_scopes = ['user-top-read']
body_params = {
'grant_type' : grant_type,
'scope' : your_scopes
}


os.environ['SPOTIPY_CLIENT_ID']= cid
os.environ['SPOTIPY_CLIENT_SECRET']= secret
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:8888/callback/'

username = "YOURACCOUNTHERE" #you can use a prompt for this if you want
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
scope = 'user-top-read'
token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)


genres = []
favorites = []
times = ['short','medium','long']

tot_dance = []
tot_energy = []
tot_loudness = []
tot_speechiness = []
tot_acousticness = []
tot_instru = []
tot_live = []
tot_valence = []
tot_tempo = []
tot_tsig = []
tot_key = []
top_150 = []
for t in times:
    top = sp.current_user_top_tracks(limit=50,offset=0,time_range='{0}_term'.format(t))
    track_ids = []
    for track in top['items']:
        track_ids.append(track['id'])
    track_info = sp.audio_features(track_ids)

    track_ids = []
    for i in track_info:
        for r in top['items']:
            if r['id'] == i['id']:

                tmp = r.copy()
                tmp.update(i)
                if tmp not in top_150:
                    top_150.append(tmp)
                    tot_dance.append(i["danceability"])
                    tot_energy.append(i["energy"])
                    tot_loudness.append(i["loudness"])
                    tot_speechiness.append(i["speechiness"])
                    tot_acousticness.append(i["acousticness"])
                    tot_instru.append(i["instrumentalness"])
                    tot_live.append(i["liveness"])
                    tot_valence.append(i["valence"])
                    tot_tempo.append(i["tempo"])
                    tot_tsig.append(i["time_signture"])
                    tot_key.append(i['key'])     3

avgs = {
'key' : tot_key/len(top_150),
'danceability' : tot_dance/len(top_150),
'energy' : tot_energy/len(top_150),
'loudness' : tot_loudness/len(top_150),
'speechiness' : tot_acousticness/len(top_150),
'acousticness' : tot_acousticness/len(top_150),
'instrumentalness' : tot_instru/len(top_150),
'liveness' : tot_live/len(top_150),
'valance' : tot_valence/len(top_150),
'tempo' : tot_tempo/len(top_150),
'tsig' : tot_tsig/len(top_150)
}

print(avgs)

# for track in top_150:
#     print(track)
#     print("\n\n")

list_of_results = top_150
list_of_artist_names = []
list_of_artist_uri = []
list_of_song_names = []
list_of_song_uri = []
list_of_durations_ms = []
list_of_explicit = []
list_of_albums = []
list_of_popularity = []
list_of_keys = []
list_of_danceability = []
list_of_energy = []
list_of_loudness = []
list_of_speechiness = []
list_of_acousticness = []
list_of_instrumentalness = []
list_of_liveness = []
list_of_valance = []
list_of_tempo = []
list_of_time_signatures = []

for result in list_of_results:
    result["album"]
    this_artists_name = result["artists"][0]["name"]
    list_of_artist_names.append(this_artists_name)
    this_artists_uri = result["artists"][0]["uri"]
    list_of_artist_uri.append(this_artists_uri)
    list_of_songs = result["name"]
    list_of_song_names.append(list_of_songs)
    song_uri = result["uri"]
    list_of_song_uri.append(song_uri)
    list_of_duration = result["duration_ms"]
    list_of_durations_ms.append(list_of_duration)
    song_explicit = result["explicit"]
    list_of_explicit.append(song_explicit)
    this_album = result["album"]["name"]
    list_of_albums.append(this_album)
    song_popularity = result["popularity"]
    list_of_popularity.append(song_popularity)
    song_key = result['key']
    list_of_keys.append(song_key)
    list_of_danceability.append(result['danceability']*100)
    list_of_energy.append(result['energy']*100)
    list_of_loudness.append(result['loudness'])
    list_of_speechiness.append(result['speechiness']*100)
    list_of_acousticness.append(result['acousticness']*100)
    list_of_instrumentalness.append(result['instrumentalness']*100)
    list_of_liveness.append(result['liveness']*100)
    list_of_valance.append(result['valence']*100)
    list_of_tempo.append(result['tempo'])
    list_of_time_signatures.append(result['time_signature'])



all_songs = pd.DataFrame(
    {'artist': list_of_artist_names,
     'artist_uri': list_of_artist_uri,
     'song': list_of_song_names,
     'song_uri': list_of_song_uri,
     'duration_ms': list_of_durations_ms,
     'explicit': list_of_explicit,
     'album': list_of_albums,
     'popularity': list_of_popularity,
     'key' : list_of_keys,
     'danceability' : list_of_danceability,
     'energy' : list_of_energy,
     'loudness' : list_of_loudness,
     'speechiness': list_of_speechiness,
     'acousticness' : list_of_acousticness,
     'instrumentalness' : list_of_instrumentalness,
     'liveness' : list_of_liveness,
     'valance' : list_of_valance,
     'tempo' : list_of_tempo,
     'time_signature' : list_of_time_signatures
    })

all_songs_saved = all_songs.to_csv('top_tracks_songs.csv')

top_tracks = all_songs

descending_order_artists = top_tracks['artist'].value_counts().sort_values(ascending=False).index
print(descending_order_artists)
descending_order_valance = top_tracks['valance'].value_counts().sort_values(ascending=False).index
descending_order_key = top_tracks['key'].value_counts().sort_values(ascending=False).index
descending_order_popularity = top_tracks['popularity'].value_counts().sort_values(ascending=False).index
descending_order_tempo = top_tracks['tempo'].value_counts().sort_values(ascending=False).index

things_to_plot = ['popularity','valance','danceability','energy','speechiness','acousticness']
plt.figure(1)
for attrib in top_tracks:
    if attrib in things_to_plot:
        thing = sb.distplot(
                top_tracks[attrib],
                kde=True,
                label=attrib,
                bins=None,
                hist=False
                )

        thing.set_xlim(0,100)
        thing.set_title(
            'My Top Track Analysis',
            fontsize=16,
            fontweight='heavy'
            )
        thing.set_xlabel('Percent')
        thing.set_xticks(range(0,100,10))

fig1_text = ""
for avg in avgs:
    if avg in things_to_plot:
        fig1_text +="Average {0}={1}%\n".format(avg,round(avgs[avg]*100),0)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(0.72, 0.80, fig1_text, transform=thing.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)
plt.legend()
plt.grid()
plt.figure(2)
hve = sb.jointplot(
    x='valance',
    y='energy',
    data=top_tracks,
    kind="reg",
    truncate=False,
    xlim=(0,100),
    ylim=(0,100),
    height=7
)
plt.show()
