# 1. mp3 파일로 저장하는 방식
# pip install gtts
# pip install playsound

from gtts import gTTS

def speak(text):
     tts = gTTS(text=text, lang='ko')
     filename='voice.mp3'
     tts.save(filename)

# main 함수
if __name__ == "__main__":
    text = '지금 보고 계시는 건물은 학생회관이며.\
          학생들이 자유롭게 토론하고 친구들과 교류할 수 있는공간입니다.'
    speak(text) # 음성으로 나오진 않고 voice.mp3 음성파일이 생성된다.

#----------------------------------------------
# 2. 직접 음성으로 말하는 방식
import pyttsx3 

class FreeTTS:
    def __init__(self, rate=180, volume=1):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate) # 음성 속도 (50~200)
        self.engine.setProperty('volume', volume) # 볼륨 (0.0 ~ 1.0)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

# main 함수
# if __name__ == "__main__":
#     tts = FreeTTS()
#     text = '안녕하세요. 저는 이루멍입니다.'
#     tts.speak(text) # mp3 음성파일로 저장되지 않고 바로 음성이 출력된다.

