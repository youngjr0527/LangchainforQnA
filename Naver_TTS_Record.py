# 초기 버전 (audio 파일을 저장하고 불러와 실행하는 방식)
from dotenv import load_dotenv
import os
import requests
import subprocess
load_dotenv() # 실제로는 main 함수에서 실행

class Naver_TTS:
    def __init__(self):
        self.client_id = os.getenv("NAVER_CLIENT_ID")
        self.client_secret = os.getenv("NAVER_CLIENT_SECRET")

    def generate_speech(self, text, file_name='NaverSpeech', speaker="nara", volume=0, speed=0, pitch=0, audio_format="mp3"):
        source_text = requests.utils.quote(text)
        data = f"speaker={speaker}&volume={volume}&speed={speed}&pitch={pitch}&format={audio_format}&text=" + source_text
        url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        
        headers = {
            "X-NCP-APIGW-API-KEY-ID": self.client_id,
            "X-NCP-APIGW-API-KEY": self.client_secret,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        response = requests.post(url, headers=headers, data=data.encode('utf-8'))
        
        folder_path = "Audio_Record"
        
        save_file = os.path.join(folder_path, f"{file_name}.mp3")
        
        if response.status_code == 200:
            print("TTS mp3 저장")
            with open(save_file, 'wb') as f:
                f.write(response.content)
            return save_file
        else:
            print(f"Error Code: {response.status_code}")
            return None

    def play_audio(self, file_path):
        try:
            absolute_path = os.path.abspath(file_path)
            
            # 윈도우에서는 'start'를 사용, Linux에서는 'afplay'을 사용
            subprocess.run(["start", absolute_path], shell=True)
            
            print(f"{file_path} 파일을 재생하였습니다.")
        except Exception as e:
            print(f"오류 발생: {e}")

if __name__ == "__main__":
    tts = Naver_TTS()
    text = "지금 보고 계시는 건물은 학생회관이며, \
        학생들이 자유롭게 토론하고 친구들과 교류할 수 있는 공간입니다."
    file_path = tts.generate_speech(text)
    if file_path:
        print(f"MP3 파일이 생성되었습니다: {file_path}")
        tts.play_audio(file_path)
