# Pyaudio 라이브러리를 이용해 mp3로 저장하는 과정 생략
from dotenv import load_dotenv
import os
import requests
import pyaudio
from pydub import AudioSegment
import io

load_dotenv() # 실제로는 main 함수에서 실행

class TTS_Agent:
    HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    URL = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"

    def __init__(self, voice="nihyun"): #nmeow, nwoof
        self.client_id = os.getenv("NAVER_CLIENT_ID")
        self.client_secret = os.getenv("NAVER_CLIENT_SECRET")
        self.HEADERS["X-NCP-APIGW-API-KEY-ID"] = self.client_id
        self.HEADERS["X-NCP-APIGW-API-KEY"] = self.client_secret
        self.voice = voice
        self.p = pyaudio.PyAudio()

    def generate_audio_and_play(self, text, volume=0, speed=0, pitch=0, audio_format="mp3"):
        print("streaming text: ", text)
        data = {
            "speaker": self.voice,
            "volume": volume,
            "speed": speed,
            "pitch": pitch,
            "format": audio_format,
            "text": text
        }
        response = requests.post(self.URL, headers=self.HEADERS, data=data)

        if response.status_code == 200:
            print("Speaking...")
            self.stream_audio(response.content)
        else:
            print(f"Error Code: {response.status_code}")

    def stream_audio(self, audio_data):
        try:
            audio = AudioSegment.from_mp3(io.BytesIO(audio_data))
            audio = audio.set_channels(1).set_frame_rate(22050)
            audio_data = audio.raw_data

            stream = self.p.open(format=self.p.get_format_from_width(audio.sample_width),
                                 channels=1,
                                 rate=22050,
                                 output=True
                                 )
            stream.write(audio_data)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if stream:
                stream.stop_stream()
                stream.close()

if __name__ == "__main__":
    tts = TTS_Agent()
    text = "여기 보이는 건물은 학생회관이며, \
        학생들이 자유롭게 토론하고 친구들과 만날 수 있는 공간입니다."
    tts.generate_audio_and_play(text)

