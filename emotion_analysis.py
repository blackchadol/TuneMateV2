import requests

API_URL = "https://api-inference.huggingface.co/models/matthewburke/korean_sentiment"
headers = {"Authorization": "Bearer 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"}

def query_hugging_face(input_text):
    response = requests.post(API_URL, headers=headers, json={"inputs": input_text})
    output = response.json()

    # 긍정적인 감정 분석 결과만 추출 (LABEL_1의 score 값)
    for result in output[0]:
        if result['label'] == "LABEL_1":  # 긍정적일 때
            return result['score']  # 긍정의 score만 반환

    return 0  # LABEL_1이 없거나 긍정적이지 않을 때 0 반환