import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from dotenv import load_dotenv
import os
import random
from spotipy.exceptions import SpotifyException
import openai
load_dotenv()
# OpenAI API 설정
openai.api_key = os.getenv('OPENAI_API_KEY')
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


# 환경 변수 로드
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
cid = CLIENT_ID
secret = CLIENT_SECRET
redirect_uri = REDIRECT_URI
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect_uri, scope="playlist-modify-public,user-modify-playback-state,user-read-playback-state"))
#Spotify API 인증
def authenticate_spotify():
    cid = CLIENT_ID
    secret = CLIENT_SECRET
    redirect_uri = REDIRECT_URI
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect_uri, scope="playlist-modify-public,user-modify-playback-state,user-read-playback-state"))
    return sp

def search_tracks(valence_min, valence_max, energy_min, energy_max, danceability_min, danceability_max, tempo_min, tempo_max):
    """
    Spotify API에서 주어진 조건에 맞는 트랙을 검색합니다.
    """
    query = f"valence:{valence_min}-{valence_max} energy:{energy_min}-{energy_max} danceability:{danceability_min}-{danceability_max} tempo:{tempo_min}-{tempo_max}"

    results = sp.search(q=query, type='track', limit=50)
    track_ids = [track['id'] for track in results['tracks']['items']]
    return track_ids


def create_playlist_with_tracks(track_ids):
    """
    Spotify에 플레이리스트를 생성하고 트랙을 추가합니다.
    """
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user=user_id, name='Generated Playlist', public=True)
    sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist['id'], tracks=track_ids)
    print(f"Playlist '{playlist['name']}' created with {len(track_ids)} tracks.")
    print(f"링크: {playlist['external_urls']['spotify']}")
    return playlist['external_urls']['spotify']


def generate_playlist_based_on_sentiment(sentiment_score):
    """
    사용자의 긍정도에 따라 valence, energy, danceability 조건을 계산하고
    플레이리스트를 생성합니다.
    """
    valence_min = max(0, sentiment_score - 0.1)
    valence_max = min(1, sentiment_score + 0.1)
    energy_min = 0.0  # 기본값 설정
    energy_max = 1.0  # 기본값 설정
    danceability_min = 0.0  # 기본값 설정
    danceability_max = 1.0
    tempo_min = 40 # 기본값 설정
    tempo_max = 200  # 기본값 설정

    if sentiment_score < 0.3:  # 낮은 긍정도
        energy_max = 0.5
        danceability_max = 0.3
        tempo_max = 100  # BPM 100 이하로 설정
    elif sentiment_score > 0.7:  # 높은 긍정도
        energy_min = 0.5
        danceability_min = 0.7
        tempo_min = 100  

    else:  # 중간 긍정도
        energy_min = 0.0
        energy_max = 1.0
        danceability_min = 0.0
        tempo_min = 40 # 기본값 설정
        tempo_max = 200  # 기본값 설정


    track_ids = search_tracks(
        valence_min=valence_min,
        valence_max=valence_max,
        energy_min=energy_min,
        energy_max=energy_max,
        danceability_min=danceability_min,
        danceability_max=danceability_max,
        tempo_min = tempo_min,
        tempo_max = tempo_max
    )

    if not track_ids:
        print("No tracks found matching the criteria.")
        return None

    return create_playlist_with_tracks(track_ids)


def generate_playlist_based_on_valence(valence_score):

    # Step 2: GPT API로 노래 제목 추천
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a music recommendation assistant."},
            {"role": "user", "content": f"Recommend 5 existing songs for an emotion score of {valence_score}. Only Provide both the song titles and their artists. Ensure these songs are available on Spotify."}
        ],
        max_tokens=100
    )

    # GPT 응답 파싱
    song_list = response.choices[0].message.content.split("\n")
    songs = [line.split("by") for line in song_list if "by" in line]
    songs = [{"title": song[0].strip(), "artist": song[1].strip()} for song in songs]

    # GPT로부터 추천받은 노래 제목 추출
    song_titles = response.choices[0].message.content.split("\n")
    song_titles = [title.strip() for title in song_titles if title.strip()]
    print("Recommended Songs:", song_titles)

    # Spotify에서 노래 검색 및 URI 추출
    song_uris = []
    for song in songs:
        query = f"{song['title']} {song['artist']}"
        results = sp.search(q=query, type="track", limit=1)
        if results['tracks']['items']:
            song_uri = results['tracks']['items'][0]['uri']
            song_uris.append(song_uri)
            print(f"Found: {song['title']} by {song['artist']}")

    # 플레이리스트 생성 및 URL 반환
    if song_uris:
        user_id = sp.current_user()['id']
        playlist = sp.user_playlist_create(user=user_id, name="Valence Playlist", public=False)
        sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)

        # 생성된 플레이리스트 URL 가져오기
        playlist_url = playlist['external_urls']['spotify']
        print(f"Playlist URL: {playlist_url}")
        return playlist_url
        # Spotify 웹 플레이어로 열기
        #webbrowser.open(playlist_url)
    else:
        print("No songs found on Spotify.")
        return None


