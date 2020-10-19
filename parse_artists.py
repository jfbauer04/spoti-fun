import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from operator import itemgetter

with open('top50_data.json') as f:
  data = json.load(f)


for term in data:

    list_of_artists = []
    list_of_genres = []
    list_of_popularity = []
    list_of_followers = []
    genres = []


    for artist in data[term]:
        list_of_artists.append(artist['name'])
        list_of_popularity.append(artist['popularity'])
        list_of_followers.append(artist['followers'])
        list_of_genres.append(artist['genres'])

        for g in artist['genres']:
            if not any(g in d.values() for d in genres):
                genres.append({'genre':g,'count':1})
            else:
                for item in genres:
                    if item['genre'] == g:
                        item['count']+=1


    my_artists = pd.DataFrame(
        {'artist': list_of_artists,
         'genres': list_of_genres,
         'popularity': list_of_popularity,
         'followers': list_of_followers
         })

    my_artists.to_csv('my_artists_'+term+'.csv')
final = sorted(genres, key=itemgetter('count'))


#descending_order_valance = my_artists['valance'].value_counts().sort_values(ascending=False).index
#descending_order_key = my_artists['key'].value_counts().sort_values(ascending=False).index
descending_order_popularity = my_artists['popularity'].value_counts().sort_values(ascending=False).index
#descending_order_tempo = my_artists['tempo'].value_counts().sort_values(ascending=False).index


ax = sb.countplot(y = my_artists['artist'], order=descending_order_popularity)

sb.despine(fig=None, ax=None, top=True, right=True, left=False, trim=False)
sb.set(rc={'figure.figsize':(6,7.2)})

ax.set_ylabel('')
ax.set_xlabel('')
ax.set_title('My Most Popular Artists', fontsize=16, fontweight='heavy')
sb.set(font_scale = 1.4)
ax.axes.get_xaxis().set_visible(False)
ax.set_frame_on(False)

y = my_artists['artist'].value_counts()
for i, v in enumerate(y):
    ax.text(v + 0.2, i + .16, str(v), color='black', fontweight='light', fontsize=14)

plt.savefig('my_artists_songs_per_artist.jpg', bbox_inches="tight")
