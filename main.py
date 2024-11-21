from emotion_analysis import query_hugging_face
from spotify_control import search_tracks_by_valence, create_playlist_with_tracks

def main():
    # 사용자로부터 텍스트 입력 받기
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

if __name__ == "__main__":
    main()
