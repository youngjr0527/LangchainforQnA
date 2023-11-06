import argparse
import logging
from threading import Thread
from naver_TTS import TTS_Agent
from google_STT import STT_Agent
from Integrate_LangChain import CampusGuideBot
from bringMenu import UOSMenuScraper
from bringNotice import UOSNoticeScraper
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)-7s : %(message)s\n')

parser = argparse.ArgumentParser()
parser.add_argument('--update', type=bool, default=False, help='Update LLM with Chroma DataBase')
args = parser.parse_args()
update_LLM = False

# main 함수
if __name__ == "__main__":
    stt = STT_Agent()
    bot = CampusGuideBot()
    tts = TTS_Agent()
    
    if args.update or update_LLM:
        logging.info("Updating LLM...")
        menu_scraper = UOSMenuScraper(save_dir='UOS_DB')
        notice_scraper = UOSNoticeScraper(save_dir='UOS_DB')
        menu_scraper.run()
        notice_scraper.run()
        bot.ingest_documents()
        logging.info("LLM updated!")
        
    stt.setup_mic()
    while True:
        # TODO: Event 발생시 정적 Action 실행하는 코드 추가. 이것도 Thread로 해서 동시에 실행하면 될듯  
        if stt.listen_for_trigger():
            logging.info("호출 명령어가 인식되었습니다.")
            tts.generate_audio_and_play("네, 무엇을 도와드릴까요?")
            task_text = stt.listen_for_task()
            if task_text:
                filtered_task = stt.filtering_task(task_text)
            print('@@@@@@@@@@@@',task_text)
            print('@@@@@@@@@@@@',filtered_task)
            if filtered_task:
                if filtered_task is None:
                    tts.generate_audio_and_play("죄송해요, 잘 못 알아들었어요. 다시 말씀해주세요.")
                    continue  # TODO: 시 호출명령어부터 말해야하는지 아니면 질문만 다시 말할지 결정해야 함

                elif filtered_task.startswith("Q"):
                    answer_text = bot.generate_answer(question=filtered_task[2:])
                    logging.info(f"[출력된 text]: {answer_text}")
                    tts.generate_audio_and_play(answer_text)

                elif filtered_task.startswith("M"):
                    tts.generate_audio_and_play(f"{filtered_task[2:]}까지 안내할게요. 저를 따라오세요")
                    # TODO: 길 안내하는 ROS 토픽을 보내는 코드 추가

                elif filtered_task == "SL":
                    tts.generate_audio_and_play("조금 천천히 걸을게요.")
                    # TODO: 속도를 늦추는 ROS 토픽을 보내는 코드 추가

                elif filtered_task == "SF":
                    tts.generate_audio_and_play("더 빨리 달려볼게요.")
                    # TODO: 속도를 높이는 ROS 토픽을 보내는 코드 추가

                elif filtered_task == "No":
                    tts.generate_audio_and_play("그것에 관해 답해드릴 수 없어요. 다른 질문을 해주세요.")
                
                elif filtered_task == "D":
                    tts.generate_audio_and_play("춤추는 중입니다.")
                    # TODO : 춤추는 ROS 토픽을 보내는 코드 추가

                else:
                    logging.error("### Unexpected input: {}".format(task_text))
                    break
            else:
                continue
        else:
            continue
