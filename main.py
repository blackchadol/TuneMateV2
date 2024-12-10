from emotion_analysis import query_hugging_face
from spotify_control import SpotifyPlayer
from librespot_control import start_librespot, check_device_connection, terminate_librespot
from spotify_playlist_generate import generate_playlist_based_on_sentiment, authenticate_spotify
from audio_output import get_audio_input  # 음성 입력 처리 모듈
from detect_keyword_and_command import detect_keyword  # 키워드 탐지 모듈
import threading

def main():
    sp = authenticate_spotify()
    player = SpotifyPlayer(sp)

    # librespot 시작 및 연결 대기
    process = start_librespot()
    print("Waiting for device to connect...")
    check_device_connection(sp)

    # 음성 명령 감지용 스레드
    keyword_thread = threading.Thread(target=detect_keyword, daemon=True)
    keyword_thread.start()

    while True:
        # 키워드 탐지
        if detect_keyword():  # '튠메야' 키워드 탐지
            # 음성 입력 받기
            input_text = get_audio_input()
            if not input_text:
                print("입력된 텍스트가 없습니다.")
                continue

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

    terminate_librespot(process)

# 프로그램 시작
if __name__ == "__main__":
    main()
