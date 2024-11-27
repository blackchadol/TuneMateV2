import subprocess
import threading
import time
import spotipy

def start_librespot():
    """librespot 명령어를 실행하는 함수 (비동기 처리)"""
    command = ["../librespot/target/release/librespot", "-n", "TuneMate", "-b", "160", "-c", "./cache"]
    
    # subprocess로 librespot 실행
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # 별도의 스레드에서 출력 처리 (출력 메시지 확인)
    def read_output():
        while True:
            stdout = process.stdout.readline()
            if stdout == b'' and process.poll() is not None:
                break
            if stdout:
                print(stdout.decode().strip())
                
        stderr = process.stderr.read()
        if stderr:
            print(stderr.decode().strip())
    
    # 출력 읽기 스레드 시작
    threading.Thread(target=read_output, daemon=True).start()
    
    return process

def check_device_connection(sp):
    """Spotify 장치 연결 상태를 확인하는 함수 (연결될 때까지 대기)"""
    while True:
        devices = sp.devices()['devices']
        if devices:
            print(f"Connected to device: {devices[0]['name']}")
            return True
        else:
            print("No device connected. Waiting for device connection...")
            time.sleep(2)  # 2초마다 다시 확인

import subprocess

def terminate_librespot(process):
    """librespot 프로세스를 종료하는 함수"""
    if process:
        print("Terminating librespot process...")
        process.terminate()  # 프로세스를 정상 종료
        # 또는 강제로 종료할 경우 아래의 주석을 해제
        # process.kill()  
    else:
        print("No process to terminate.")
