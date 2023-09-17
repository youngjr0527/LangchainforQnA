# # pip install gtts
# # pip install playsound
# from gtts import gTTS

# 1. mp3 파일로 저장하는 방식
# # import playsound

# def speak(text):
#      tts = gTTS(text=text, lang='ko')
#      filename='voice.mp3'
#      tts.save(filename)
#      # playsound.playsound(filename) # 음성으로 바로 출력하는 기능인데 설치가 안된다..

# # main 함수
# text = '안녕하세요. 저는 이루멍입니다.'
# speak(text) # 음성으로 나오진 않고 voice.mp3 음성파일이 생성된다.

#----------------------------------------------
# 2. 직접 음성으로 말하는 방식
import pyttsx3 

class TextToSpeech:
    def __init__(self, rate=200, volume=1):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate) # 음성 속도 (50~200)
        self.engine.setProperty('volume', volume) # 볼륨 (0.0 ~ 1.0)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

# main 함수
if __name__ == "__main__":
    tts = TextToSpeech(rate=200, volume=1)
    text = '안녕하세요. 저는 이루멍입니다.'
    tts.speak(text) # mp3 음성파일로 저장되지 않고 바로 음성이 출력된다.