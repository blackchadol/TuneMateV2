from emotion_analysis import query_hugging_face
from spotify_control import SpotifyPlayer
from librespot_control import start_librespot, check_device_connection, terminate_librespot
from spotify_playlist_generate import generate_playlist_based_on_sentiment, authenticate_spotify, generate_playlist_based_on_valence
from audio_output import get_audio_input
from led_control import EmotionLED  # LED 컨트롤 클래스 import
import threading

def main():
    # LED 컨트롤러 초기화
    emotion_led = EmotionLED()

    sp = authenticate_spotify()
    player = SpotifyPlayer(sp)
    
    # librespot 시작 및 연결 대기
    process = start_librespot()
    print("Waiting for device to connect...")
    check_device_connection(sp)
    
    #try:
    #while True:
        # 테스트를 위해 음성 인식 대신 텍스트 입력 사용
    input_text = None
    while input_text is None:
        input_text = get_audio_input()  # 음성 입력 받기
            
        # if input_text.lower() == 'q':  # 종료 조건
        #     break
        
    if input_text:
            # 감정 분석 수행
            valence_score = query_hugging_face(input_text)
            valence_score = round(valence_score, 1)
            print(f"분석된 감정 점수: {valence_score}")
            
            # LED 업데이트
            emotion_led.update_lights(valence_score)
            
            if valence_score > 0.5:
                print("긍정적인 감정으로 분석됨. 음악을 재생합니다.")
            else:
                print("부정적인 감정으로 분석됨. 음악을 재생합니다.")
            
            # 플레이리스트 생성 및 재생
            playlist_url = generate_playlist_based_on_valence(valence_score)
            print(f"플레이리스트 생성 완료! 링크: {playlist_url}")
            
            player.play_track(playlist_url)

    # while문을 나와서 handle_user_input() 실행
    player.handle_user_input()

#except KeyboardInterrupt:
    #print("\n프로그램을 종료합니다.")
#finally:
    terminate_librespot(process)
    emotion_led.clear_lights()
    


if __name__ == "__main__":
    main()
