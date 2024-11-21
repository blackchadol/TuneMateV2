import spotipy
from spotipy.oauth2 import SpotifyOAuth
#from nlp import genre

cid = 'bad5081179454c7aac97e6f6eabbb794'
secret = '0aa836ce7d22486c8e2b5b51dec47687'
redirect_uri = 'http://localhost:8080/callback'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect_uri,  scope="playlist-modify-public"))


# valence에 따라 트랙 검색 함수 (장르 제외)
def search_tracks_by_valence(valence_score):
    # valence에 따른 트랙 검색 (50곡 한정)
    """
    valence_score 값을 바탕으로 Spotify에서 음악을 검색합니다.
    valence 값은 0 (슬픔)에서 1 (행복)까지의 값을 가집니다.
    """
    results = sp.search(q=f"valence:{valence_score}", type='track', limit=50)
    track_ids = [track['id'] for track in results['tracks']['items']]
    
    return track_ids



## Spotify에 플레이리스트 생성하고 트랙 추가
def create_playlist_with_tracks(track_ids):
    """
    검색된 트랙 ID들을 바탕으로 Spotify에 플레이리스트를 생성하고 트랙을 추가합니다.
    """
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user=user_id, name='Generated Playlist', public=True)
    
    # 플레이리스트에 트랙 추가
    sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist['id'], tracks=track_ids)
    print(f"Playlist '{playlist['name']}' created with {len(track_ids)} tracks.")
    print(f"링크: {playlist['external_urls']['spotify']}")
    return playlist['external_urls']['spotify']