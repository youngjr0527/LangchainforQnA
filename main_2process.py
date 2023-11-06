import argparse
import logging
from multiprocessing import Process, Event
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

def process_A(event):
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

    while not event.is_set():  # Event가 set 상태가 아닐 때만 실행
        if stt.listen_for_trigger():
            logging.info("호출 명령어가 인식되었습니다.")
            tts.generate_audio_and_play("네, 무엇을 도와드릴까요?")
            task_text = stt.listen_for_task()
            logging.info(f"input text: {task_text}")
            if task_text:
                filtered_task = stt.filtering_task(task_text)
            logging.info(f"filtered text: {filtered_task}")
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

                elif filtered_task == "D":
                    tts.generate_audio_and_play("춤추는 중입니다.")
                    # TODO : 춤추는 ROS 토픽을 보내는 코드 추가

                elif filtered_task == "No":
                    tts.generate_audio_and_play("그것에 관해 답해드릴 수 없어요. 다른 질문을 해주세요.")
                
                else:
                    logging.error("### Unexpected input: {}".format(task_text))
                    break
            else:
                continue
        else:
            continue

        # TODO: 프로세스 B를 시작해야 할 조건(GPS 신호가 들어오면)이 충족되면 event.set() 호출 -> True


# 프로세스 B의 함수
def process_B(event):
    # 프로세스 B의 로직
    while event.is_set():  # Event가 set 상태일 때만 실행
        # 프로세스 B의 작업 수행
        # ...
        # 각 GPS 위치에 맞는 녹음 파일을 재생 (예: 미래관 근처면 미래관 설명 녹음 파일 재생)
        # ...
        # 프로세스 A를 재개해야 할 조건이 충족되면 event.clear() 호출
        pass

# main 함수
if __name__ == "__main__":
    event = Event()  
    # event가 발생하면(GPS 신호가 들어와 멘트를 출력해야 할 때) set() 호출
    # event.set() 호출하여 event 상태가 True가 되면 Process B가 실행됨
    # event.clear() 호출하여 event 상태가 False가 되면 Process A가 실행됨
    
    # 프로세스 A와 B 시작
    pa = Process(target=process_A, args=(event,))
    pb = Process(target=process_B, args=(event,))
    event.clear() # 우선 프로세스 A부터 실행
    pa.start()
    pb.start()

    # 프로세스들이 종료될 때까지 기다림
    pa.join()
    pb.join()


    