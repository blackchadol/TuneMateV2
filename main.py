from emotion_analysis import query_hugging_face
from spotify_control import SpotifyPlayer
from librespot_control import start_librespot, check_device_connection, terminate_librespot
from spotify_playlist_generate import generate_playlist_based_on_sentiment, authenticate_spotify
from audio_output import get_audio_input  # 음성 입력 모듈 가져오기

# 메인 함수
def main():
    # Spotify 인증 및 플레이어 초기화
    sp = authenticate_spotify()
    player = SpotifyPlayer(sp)
    
    # Librespot 실행
    print("Starting librespot...")
    process = start_librespot()

    # Librespot 기기 연결 확인
    print("Waiting for device to connect...")
    check_device_connection(sp)

    # 음성 입력 받기
    input_text = get_audio_input()  # 마이크 입력으로 텍스트 변환
    if not input_text:
        print("입력된 텍스트가 없습니다. 프로그램을 종료합니다.")
        return

    # 감정 분석 수행
    valence_score = query_hugging_face(input_text)
    print(f"분석된 감정 점수: {valence_score}")
    if valence_score > 0.5:
        print("긍정적인 감정으로 분석됨. 음악을 재생합니다.")
    else:
        print("부정적인 감정으로 분석됨. 음악을 재생합니다.")
    
    # valence_score에 맞는 음악 트랙을 검색하여 플레이리스트 생성
    playlist_url = generate_playlist_based_on_sentiment(valence_score)
    print(f"플레이리스트 생성 완료! 링크: {playlist_url}")

    # 플레이리스트 재생
    player.play_track(playlist_url)

    # 사용자 입력에 따른 명령 처리
    player.handle_user_input()

    # Librespot 종료
    terminate_librespot(process)

# 프로그램 시작
if __name__ == "__main__":
    main()
