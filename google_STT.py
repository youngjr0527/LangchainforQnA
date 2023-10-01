#pip install SpeechRecognition
#pip install pyaudio
#pip install pydub

import logging
from speech_recognition import Recognizer, Microphone

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)-7s : %(message)s\n')

class SpeechToText:
    def __init__(self, trigger_word, lang="ko-KR"):
        self.r = Recognizer()    ## 다른 API로 대체할 예정
        self.mic = Microphone()  ## 계속 사용할 예정
        self.trigger_word = trigger_word # 호출 명령어
        self.lang = lang

    def recognize_voice(self):
        try:
            with self.mic as source:
                logging.info("주변 소음을 측정합니다.")
                self.r.adjust_for_ambient_noise(source)
                logging.info("소음 측정 완료. 음성 인식을 시작합니다.")
                audio = self.r.listen(source, timeout=5, phrase_time_limit=10)

            text = self.r.recognize_google(audio, language=self.lang)
            logging.info("[수집된 음성]: {}".format(text))

            if self.trigger_word in text:
                logging.info("호출 명령어가 인식되었습니다. 질문을 기다립니다.")
                with self.mic as source:
                    logging.info("질문을 말하세요.")
                    audio = self.r.listen(source, timeout=5, phrase_time_limit=5)
                question_text = self.r.recognize_google(audio, language=self.lang)
                logging.info("[질문 내용]: {}".format(question_text))
                return question_text
            else:
                logging.info("호출 명령어가 없습니다. 다시 시도하세요.")
                return None
            
        except:
            logging.info("타임아웃: 음성 감지 없음. 다시 while문 반복")
            return None

# main 함수
if __name__ == "__main__":
    trigger_word = "안녕 이루" 
    stt = SpeechToText(trigger_word)

    while True:
        text = stt.recognize_voice()
        if text:
            logging.info("[입력된 text]: {}".format(text))
            break
