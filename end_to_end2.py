import logging
from Naver_TTS import NaverTTS
from build_langchain import QARetrieval
from whisper_test4 import Whisper_STT_Agent
# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)-7s : %(message)s\n')

# main 함수
if __name__ == "__main__":
    qa_system = QARetrieval(db_path="./Chroma_DB")
    # qa_system.ingest_documents()  # ingest는 매번 할 필요 없음
    
    tts = NaverTTS(rate=190, volume=1)

    while True:
        agent = Whisper_STT_Agent()
        agent.listen_and_detect()
        if question_text:
            logging.info("[입력된 text]: {}".format(question_text))
            break

    qa_system = QARetrieval(db_path="./chroma_db")
    answer_text = qa_system.generate_answer(question=question_text)
    
    logging.info("[출력된 text]: {}".format(answer_text))
    file_path = tts.generate_speech(answer_text)
    if file_path:
        print(f"MP3 파일이 생성되었습니다: {file_path}")
        tts.play_audio(file_path)


