from emotion_analysis import query_hugging_face
from spotify_control import search_tracks_by_valence, create_playlist_with_tracks, authenticate_spotify
from spotify_control import SpotifyPlayer
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
from librespot_control import start_librespot, check_device_connection, terminate_librespot



def main():
    # 사용자로부터 텍스트 입력 받기
    sp = authenticate_spotify()
    player = SpotifyPlayer(sp)
    # librespot 실행
    print("Starting librespot...")
    process = start_librespot()

    print("Waiting for device to connect...")
    check_device_connection(sp)

    input_text = input("감정을 입력하세요: ")

    # 감정 분석 수행
    valence_score = query_hugging_face(input_text)
    print(valence_score)
    if valence_score > 0.5:
        print("긍정적인 감정으로 분석됨. 음악을 재생합니다.")
    else:
        print("부정적인 감정으로 분석됨. 음악을 재생합니다.")
    
    # valence_score에 맞는 음악 트랙을 검색
    track_ids = search_tracks_by_valence(valence_score)

    # 검색된 트랙들을 바탕으로 플레이리스트 생성
    playlist_url = create_playlist_with_tracks(track_ids)
    print(f"플레이리스트 생성 완료! 링크: {playlist_url}")
    # 플레이리스트 재생
    player.play_track(playlist_url)
    
    # 사용자 입력에 따른 명령 처리
    player.handle_user_input()

    terminate_librespot(process)

   
    

if __name__ == "__main__":
    main()
    
