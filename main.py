# OpenAI Whisper + Naver Voice 
import argparse
import logging
from threading import Thread
from Whisper_STT import Whisper_STT
from Integrate_LangChain import CampusGuideBot
from Naver_TTS import Naver_TTS
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)-7s : %(message)s\n')

parser = argparse.ArgumentParser()
parser.add_argument('--update', type=bool, default=False, help='Update LLM with Chroma DataBase')
args = parser.parse_args()

# Whisper에서 발생하는 UserWarning 무시
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# main 함수
if __name__ == "__main__":
    tts = Naver_TTS()
    stt = Whisper_STT()
    bot = CampusGuideBot()
    if args.update:
        logging.info("Updating LLM...")
        bot.ingest_documents()
    
    while True:
        # TODO: Event 발생시 정적 Action 실행하는 코드 추가. 이것도 Thread로 해서 동시에 실행하면 될듯  

        stt.wakeup_event.clear() # wakeup_event를 False로 초기화
        Thread(target=stt.listening_for_wakeup_word).start()
        stt.wakeup_event.wait() # wakeup_event가 True가 될 때까지 대기

        logging.info("Wakeup word detected!")
        tts.generate_audio_and_play("네, 무엇을 도와드릴까요?")
        processed_Q = stt.listen_for_task()

        # processed_Q = "SL"

        if processed_Q.startswith("Q"):
            answer_text = bot.generate_answer(question=processed_Q[2:])
            logging.info(f"[출력된 text]: {answer_text}")
            tts.generate_audio_and_play(answer_text)

        elif processed_Q.startswith("M"):
            tts.generate_audio_and_play(f"{processed_Q[2:]}까지 안내할게요. 저를 따라오세요")
            # TODO: 길 안내하는 ROS 토픽을 보내는 코드 추가
        
        elif processed_Q == "SL":
            tts.generate_audio_and_play("조금 천천히 걸을게요.")
            # TODO: 속도를 늦추는 ROS 토픽을 보내는 코드 추가
            
        elif processed_Q == "SF":
            tts.generate_audio_and_play("더 빨리 달려볼게요.")
            # TODO: 속도를 높이는 ROS 토픽을 보내는 코드 추가
            
        else:
            logging.error("Unexpected input: {}".format(processed_Q))
            break

