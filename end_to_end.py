import logging
from google_TTS import TextToSpeech
from google_STT import SpeechToText
from build_langchain import QARetrieval

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)-7s : %(message)s\n')

# main 함수
if __name__ == "__main__":
    qa_system = QARetrieval(db_path="./chroma_db")
    # qa_system.ingest_documents()  # ingest는 매번 할 필요 없음
    
    trigger_word = "하이 빅스비" # "안녕 이루멍"이라고 정확히 인식을 잘 못함
    stt = SpeechToText(trigger_word)
    tts = TextToSpeech(rate=190, volume=1)

    while True:
        question_text = stt.recognize_voice()
        if question_text:
            logging.info("[입력된 text]: {}".format(question_text))
            break

    qa_system = QARetrieval(db_path="./chroma_db")
    answer_text = qa_system.generate_answer(question=question_text)
    
    logging.info("[출력된 text]: {}".format(answer_text))
    tts.speak(answer_text)


