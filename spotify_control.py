import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

#from nlp import genre

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

class SpotifyPlayer:
    def __init__(self, sp):
        self.sp = sp
        self.track_list = []  # 트랙 리스트
        self.current_track_index = 0  # 현재 트랙 인덱스
        self.is_playing = False  # 재생 상태

    def play_track(self, spotify_url):
   
    
        track_uri = None  # 트랙 URI 초기화
        track_list = []  # 트랙 리스트 초기화

        if "track" in spotify_url:
        # 트랙 URL이면, track_id 추출하여 URI 형식으로 변환
            track_uri = spotify_url.split('/')[-1]  # 'https://open.spotify.com/track/{track_id}'에서 {track_id} 추출
            track_uri = f"spotify:track:{track_uri}"
            track_list.append(track_uri)  # 트랙 리스트에 추가
        elif "playlist" in spotify_url:
        # 플레이리스트 URL이면, 플레이리스트 ID로부터 트랙들 추출
            playlist_id = spotify_url.split('/')[-1]  # 'https://open.spotify.com/playlist/{playlist_id}'에서 {playlist_id} 추출
            playlist_tracks = sp.playlist_tracks(playlist_id)['items']
        
            if playlist_tracks:
            # 각 트랙 URI를 리스트에 추가
                for track in playlist_tracks:
                    track_list.append(track['track']['uri'])
            else:
                print("플레이리스트에 트랙이 없습니다.")
                return
        else:
            print("지원하지 않는 URL 형식입니다.")
            return
        self.track_list = track_list  # 생성된 트랙 리스트 저장
        self.start_playback(self.track_list[self.current_track_index])  # 첫 번째 트랙 재생

    def start_playback(self, track_uri):
        """트랙을 재생하는 함수"""
        devices = self.sp.devices()["devices"]
        if devices:
            device_id = devices[0]["id"]
            self.sp.start_playback(device_id=device_id, uris=[track_uri])
            self.is_playing = True
            print(f"Playing {track_uri} on device: {devices[0]['name']}")
        else:
            print("No active devices found.")

    def next_track(self):
        """다음 트랙 재생"""
        if self.current_track_index < len(self.track_list) - 1:
            self.current_track_index += 1
            self.start_playback(self.track_list[self.current_track_index])
        else:
            print("This is the last track in the playlist.")

    def previous_track(self):
        """이전 트랙 재생"""
        if self.current_track_index > 0:
            self.current_track_index -= 1
            self.start_playback(self.track_list[self.current_track_index])
        else:
            print("This is the first track in the playlist.")

    def pause_or_play(self):
        """재생 또는 일시 정지"""
        if self.is_playing:
            devices = self.sp.devices()["devices"]
            if devices:
                device_id = devices[0]["id"]
                self.sp.pause_playback(device_id=device_id)
                self.is_playing = False
                print("Playback paused.")
        else:
            self.start_playback(self.track_list[self.current_track_index])

    def handle_user_input(self):
        """사용자 입력 처리"""
        while True:
            # 사용자 입력 받기
            user_input = input("Enter command (n: next, p: previous, s: play/pause, q: quit): ").strip().lower()
            
            if user_input == 'n':  # 다음 트랙
                self.next_track()
            elif user_input == 'p':  # 이전 트랙
                self.previous_track()
            elif user_input == 's':  # 재생/일시 정지
                self.pause_or_play()
            elif user_input == 'q':  # 종료
                print("Exiting player.")
                break
            else:
                print("Invalid input. Please use 'n' for next, 'p' for previous, 's' for play/pause, 'q' to quit.")

            time.sleep(1)  # 사용자 입력을 확인한 후, 잠시 대기


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

