# Pyaudio 라이브러리를 이용해 mp3로 저장하는 과정 생략
from dotenv import load_dotenv
import os
import requests
import pyaudio
from pydub import AudioSegment
import io

load_dotenv() # 실제로는 main 함수에서 실행

class NaverTTS:
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.p = pyaudio.PyAudio()


    def generate_and_play_speech(self, text, speaker="nwoof", volume=0, speed=0, pitch=0, audio_format="mp3"):
        print("text: ", text)
        source_text = requests.utils.quote(text)
        data = f"speaker={speaker}&volume={volume}&speed={speed}&pitch={pitch}&format={audio_format}&text=" + source_text
        url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        
        headers = {
            "X-NCP-APIGW-API-KEY-ID": self.client_id,
            "X-NCP-APIGW-API-KEY": self.client_secret,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        response = requests.post(url, headers=headers, data=data.encode('utf-8'))

        if response.status_code == 200:
            print("TTS 스트리밍 재생")
            self.stream_audio(response.content)
        else:
            print(f"Error Code: {response.status_code}")

    def stream_audio(self, audio_data):
        audio = AudioSegment.from_mp3(io.BytesIO(audio_data))
        audio = audio.set_channels(1).set_frame_rate(22050)
        audio_data = audio.raw_data

        stream = self.p.open(format=self.p.get_format_from_width(audio.sample_width),
                             channels=1,
                             rate=22050,
                             output=True)
        stream.write(audio_data)

        stream.stop_stream()
        stream.close()

if __name__ == "__main__":
    tts = NaverTTS()
    text = "안녕하세요 저는 이루멍이에요"
    tts.generate_and_play_speech(text)

