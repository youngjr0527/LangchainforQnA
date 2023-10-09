#pip install SpeechRecognition
#pip install pyaudio
#pip install pydub
class Google_STT_old_version:
    def __init__(self, lang="ko-KR"):
        self.r = Recognizer()   
        self.mic = Microphone()  
        self.trigger_words = ["이루", "루머", "Hello", "안녕"]
        self.lang = lang

    def recognize_voice(self):
        while True:
            try:
                with self.mic as source:
                    logging.info("주변 소음을 측정합니다.")
                    self.r.adjust_for_ambient_noise(source, duration=1)
                    logging.info("소음 측정 완료. 음성 인식을 시작합니다.")
                    audio = self.r.listen(source, timeout=4, phrase_time_limit=2)

                text = self.r.recognize_google(audio, language=self.lang)
                logging.info("[수집된 음성]: {}".format(text))

                if any(trigger_word in text for trigger_word in self.trigger_words):
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

import logging
from speech_recognition import Recognizer, Microphone
import speech_recognition

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)-7s : %(message)s\n')

class Google_STT:
    def __init__(self, lang="ko-KR"):
        self.r = Recognizer()
        self.mic = Microphone()
        self.trigger_words = ["이루", "루머", "헬로", "Hello", "안녕"]
        self.lang = lang

    def setup_mic(self):
        with self.mic as source:
            logging.info("주변 소음을 측정합니다.")
            self.r.adjust_for_ambient_noise(source)
            logging.info("소음 측정 완료.")
    
    def listen_for_trigger(self):
        try:
            with self.mic as source:
                logging.info("호출 명령어를 탐지하는 중...")
                audio = self.r.listen(source, timeout=4, phrase_time_limit=2)
            text = self.r.recognize_google(audio, language=self.lang)
            logging.info("[수집된 음성]: {}".format(text))
            return any(trigger_word in text for trigger_word in self.trigger_words)
        
        except speech_recognition.UnknownValueError:
            logging.info("호출 명령어가 없습니다.")
            return False
        
        except Exception as e:
            logging.error("Error: {}".format(e))
            return False

    def listen_for_task(self):
        try:
            with self.mic as source:
                logging.info("Task을 듣는 중...")
                audio = self.r.listen(source, timeout=5, phrase_time_limit=2)
            task_text = self.r.recognize_google(audio, language=self.lang)
            logging.info("[수집된 Task 내용]: {}".format(task_text))
            return task_text
        except speech_recognition.UnknownValueError:
            logging.info("알 수 없는 값: Google 음성 인식이 결과를 반환하지 못했습니다.")
            return False
        except Exception as e:
            logging.error("Error: {}".format(e))
            return False

    def run(self):
        while True:
            if self.listen_for_trigger():
                logging.info("호출 명령어가 인식되었습니다.")
                task_text = self.listen_for_task()
                logging.info("[task 내용]: {}".format(task_text))
                break

if __name__ == "__main__":
    stt = Google_STT()
    stt.setup_mic()
    stt.run()

class Filter_STT(Google_STT):
    def __init__(self, lang="ko-KR"):
        super().__init__(lang)















