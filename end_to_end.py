import logging
from google_TTS import TextToSpeech
from google_STT import SpeechToText
from build_langchain import QARetrieval

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)-7s : %(message)s\n')

# main 함수
if __name__ == "__main__":
    qa_system = QARetrieval(db_path="./chroma_db")
    qa_system.ingest_documents()
    
    trigger_word = "하이 빅스비"
    stt = SpeechToText(trigger_word)
    tts = TextToSpeech(rate=190, volume=1)

    while True:
        question_text = stt.recognize_voice()
        if question_text:
            logging.info("[입력된 text]: {}".format(question_text))
            break

    qa_system = QARetrieval(db_path="./chroma_db")
    answer_text = qa_system.generate_answer(question=question_text)
    
    tts.speak(answer_text)


