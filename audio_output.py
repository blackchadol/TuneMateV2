import speech_recognition as sr

# 음성을 텍스트로 변환하는 함수
def get_audio_input():
    """
    USB 마이크를 통해 음성을 입력받고 텍스트로 변환합니다.

    Returns:
        str: 변환된 텍스트
        None: 음성 입력 실패 시
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()  # USB 마이크 자동 탐지

    print("마이크 준비 중... 잠시만 기다리세요.")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)  # 주변 소음 조정
        print("음성을 입력하세요:")
        try:
            # 음성 듣기
            audio = recognizer.listen(source, timeout=5)  # 5초 동안 기다림
            print("음성을 처리 중입니다...")
            
            # 음성을 텍스트로 변환
            text = recognizer.recognize_google(audio, language="ko-KR")
            print(f"변환된 텍스트: {text}")
            return text
        except sr.WaitTimeoutError:
            print("시간 초과! 음성이 입력되지 않았습니다.")
            return None
        except sr.UnknownValueError:
            print("음성을 인식할 수 없습니다.")
            return None
        except sr.RequestError as e:
            print(f"음성 인식 서비스 오류: {e}")
            return None
