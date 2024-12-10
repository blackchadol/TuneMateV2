from vosk import Model, KaldiRecognizer
import pyaudio
import json
from spotify_control import command_queue

MODEL_PATH = "vosk-model-small-ko-0.22"

def detect_keyword():
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()

    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print("음성 명령 대기 중... '튠메야'를 호출하세요.")

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            if "text" in result:
                transcript = result["text"]
                print(f"인식된 음성: {transcript}")
                if "김재영" in transcript:
                    if "다음" in transcript or "넘겨" in transcript:
                        command_queue.put("next")
                    elif "이전" in transcript:
                        command_queue.put("previous")
                    elif "멈춰" in transcript:
                        command_queue.put("pause")
                    elif "재생" in transcript:
                        command_queue.put("play")
                    elif "꺼" in transcript or "종료" in transcript:
                        command_queue.put("quit")
                    return True
