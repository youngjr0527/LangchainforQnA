# openai가 아닌 whisper를 직접 사용
#pip install -U openai-whisper

# transcript = "시립대는 동아리가 뭐 있어?" # Q:시립대는 동아리가 뭐 있어?
# transcript = "아 진짜 왤캐 느려 빨리좀 가"  # S:빨리
# transcript = "후문이 어디야"  # M:후문 

import openai
import whisper
import torch
audio_path = "./voice.mp3"
audio_file= open(audio_path, "rb")

class STT_Agent:
    def __init__(self,model_type="base"):
        self.PROMPT_FOR_SYSTEM = "너는 서울시립대학교 캠퍼스 홍보 및 길 안내 로봇이다. \
                                  만약 길 안내에 관한 입력값이면 처음에 'M:건물이나 장소만' 형태로 출력해. \
                                  만약 속도에 관한 입력값이면 'S:속도 관련 키워드만' 형태로 출력해.\
                                  이외의 입력값은 'Q:입력값' 형태로 그대로 출력해."
        self.WAKEUP_WORD_PROMPT = "너는 '이봐 이루멍'이라는 wakeup-word만 인식해야 해. \
                                   입력값 중에 '이봐 이루멍'이라는 말이 있으면 Yes를 대답. \
                                   이외의 입력값은 Ignore로 대답"
        
        self.audio_model = whisper.load_model(model_type, download_root="./.cache/whisper")

    def transcribe_audio(self, audio_file, prompt):
        return openai.Audio.transcribe("whisper-1", audio_file, prompt=prompt)["text"]
        # return self.audio_model.transcribe(audio_path, prompt=prompt)["text"]

    def chat_completion(self, model, temp, messages):
        return openai.ChatCompletion.create(
            model=model,
            temperature=temp,
            messages=messages
        )['choices'][0]['message']['content']

    def preprocess_transcript(self, audio_file):
        transcript = self.transcribe_audio(audio_file, "서울시립대")
        messages = [
            {"role": "system", "content": self.PROMPT_FOR_SYSTEM},
            {"role": "user", "content": "미래관은 어디야?"},
            {"role": "assistant", "content": "M:미래관"},
            {"role": "user", "content": "속도좀 줄여줘"},
            {"role": "assistant", "content": "S:줄임"},
            {"role": "user", "content": transcript},
        ]
        return self.chat_completion("gpt-3.5-turbo", 0, messages)

    def detect_wakeup_word(self, audio_file):
        transcript = self.transcribe_audio(audio_file, "이봐 이루멍")
        messages = [
            {"role": "system", "content": self.WAKEUP_WORD_PROMPT},
            {"role": "user", "content": "이봐 이루멍"},
            {"role": "assistant", "content": "Yes"},
            {"role": "user", "content": "학교 좋다"},
            {"role": "assistant", "content": "Ignore"},
            {"role": "user", "content": transcript}
        ]
        return self.chat_completion("gpt-3.5-turbo", 0, messages)

if __name__ == "__main__":
    bot = STT_Agent()
    audio_path = "./voice.mp3"
    audio_file = open(audio_path, "rb")

    # corrected_text = bot.preprocess_transcript(audio_file)
    # print("Preprocessed text:", corrected_text)

    wakeup_result = bot.detect_wakeup_word(audio_file)
    print("Wakeup word detection:", wakeup_result)


