import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

URL = "https://www.billboard.com/charts/hot-100/"

response = requests.get(URL, headers=HEADERS)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

div_tags = soup.find_all(name='div', class_='o-chart-results-list-row-container')

songs = []
for div_tag in div_tags:
    h3_tag = div_tag.find(name='h3', id='title-of-a-story')
    songs.append(h3_tag.get_text().strip())

print(songs)

client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.environ.get("SPOTIFY_REDIRECT_URI")
scope = "user-library-read"
# scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, cache_path="token.txt"))

user_id = sp.current_user()["id"]
print(user_id)

# as of February 2026 you need to go premium to access such resources:
# HTTP Error for GET to https://api.spotify.com/v1/me/ with Params: {} returned 403 due to
# Active premium subscription required for the owner of the app. When the subscription status changes,
# it can take a few hours before requests are allowed again.

# taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'

# results = sp.artist_albums(taylor_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = sp.next(results)
#     albums.extend(results['items'])
#
# for album in albums:
#     print(album['name'])