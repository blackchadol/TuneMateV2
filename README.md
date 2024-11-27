# TuneMate 프로젝트

## 프로젝트 개요

**TuneMate**는 사용자의 감정을 분석하여 그에 맞는 음악을 추천하고 재생하는 프로젝트이다. HuggingFace의 감정 분석 모델을 사용하여 사용자가 입력한 텍스트의 감정을 분석하고, 그에 맞는 음악을 Spotify에서 찾아서 재생할 수 있다. 이 프로젝트는 **librespot**을 이용해 Spotify와 연결하고 음악을 제어하는 기능을 제공한다.

---

## 프로젝트 구성

### 1. **main.py**
`main.py`는 이 프로젝트의 중심이 되는 파일이다. 사용자가 텍스트를 입력하면 감정을 분석하고, 그에 맞는 음악을 추천하여 재생하는 흐름을 담당한다.

### 주요 함수:
- `main()`: 프로그램의 메인 함수이다. 사용자가 텍스트를 입력하면 그 감정을 분석하고, 그 결과에 맞는 음악을 찾아서 플레이리스트를 생성하고 재생한다. 음악이 재생되는 동안 사용자는 트랙을 제어할 수 있다.

---

### 2. **librespot_control.py**
`librespot_control.py`는 Spotify 장치와의 연결을 담당하는 파일이다. 이 파일은 **librespot**을 이용하여 Spotify와 연결하고 음악을 재생하는 데 필요한 기능들을 제공한다.

### 주요 함수:
- `start_librespot()`: `librespot`을 실행하는 함수이다. 이 함수를 호출하면 `librespot`이 백그라운드에서 실행된다.
- `check_device_connection(sp)`: Spotify 장치와의 연결을 확인하는 함수이다. 장치가 연결될 때까지 대기한다.
- `terminate_librespot(process)`: 실행 중인 `librespot` 프로세스를 종료하는 함수이다. 음악 재생을 마친 후 `librespot`을 종료할 때 사용한다.

---

### 3. **emotion_analysis.py**
`emotion_analysis.py`는 사용자가 입력한 텍스트의 감정을 분석하는 파일이다. 여기서는 HuggingFace의 감정 분석 모델을 사용하여 감정 점수를 반환한다.

### 주요 함수:
- `query_hugging_face(input_text)`: 이 함수는 사용자가 입력한 텍스트의 감정을 분석하여 긍정적인 감정일 경우 점수를 반환한다. 부정적인 감정일 경우에는 0을 반환한다.

---

### 4. **spotify_control.py**
`spotify_control.py`는 Spotify API를 통해 음악을 검색하고, 플레이리스트를 생성하며, 음악을 제어하는 기능을 제공하는 파일이다.

### 주요 함수:
- `authenticate_spotify()`: Spotify API 인증을 위한 함수이다. 이 함수가 실행되면 Spotify에 인증되고, API를 통해 음악을 제어할 수 있다.
- `SpotifyPlayer`: 이 클래스는 음악을 재생하고, 트랙을 제어하는 기능을 담당한다. 예를 들어, 트랙을 재생하고, 다음 트랙이나 이전 트랙으로 넘어가거나, 일시 정지/재생을 제어할 수 있다.
- `search_tracks_by_valence(valence_score)`: 감정 분석 결과인 `valence_score`를 바탕으로 Spotify에서 트랙을 검색하는 함수이다.
- `create_playlist_with_tracks(track_ids)`: 검색된 트랙들을 바탕으로 Spotify에 플레이리스트를 생성하는 함수이다.

---

## 실행 방법

1. 먼저, 이 프로젝트를 클론한 후 필요한 라이브러리를 설치해야 한다.
   
   ```
   pip install -r requirements.txt
   ```

2. `.env` 파일을 생성하고, `CLIENT_ID`, `CLIENT_SECRET`, `REDIRECT_URI` 값을 추가해야 한다.
   
3. `main.py`를 실행하여 프로그램을 시작할 수 있다. 사용자로부터 텍스트를 입력받고, 그에 맞는 음악을 추천하여 재생한다.

   ```
   python main.py
   ```

---

## 주의 사항

- **Spotify 인증**: `main.py`가 Spotify API와 연결되려면 먼저 Spotify 계정으로 인증을 받아야 한다. `.env` 파일에 올바른 `CLIENT_ID`와 `CLIENT_SECRET`을 입력해야 한다.
- **librespot**: `librespot`이 백그라운드에서 실행되며, 이를 통해 실제 Spotify 장치와 연결되므로 `librespot`이 제대로 실행되도록 설정해야 한다.
- **감정 분석**: HuggingFace API를 통해 감정 분석을 하므로 인터넷이 연결되어 있어야 한다.

