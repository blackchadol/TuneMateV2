import re

def detect_speed(input_text):
    if re.search(r"빠ㄹ(?:르|른|르게)?", input_text):
        return "빠름"  # "빠ㄹ"이 포함된 경우
    else:
        return "느림"  # "빠ㄹ"이 없으면 느림으로 처리

# 테스트
input_text = "이 노래는 빠르게 뛰어놀 수 있을 것 같아요"
speed = detect_speed(input_text)
print(f"속도: {speed}")
