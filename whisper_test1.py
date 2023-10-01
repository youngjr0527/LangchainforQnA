#pip install -U openai-whisper

import openai
audio_path = "./voice.mp3"
audio_file= open(audio_path, "rb")

# transcript = "시립대는 동아리가 뭐 있어?" # Q:시립대는 동아리가 뭐 있어?
# transcript = "아 진짜 왤캐 느려 빨리좀 가"  # S:빨리
# transcript = "후문이 어디야"  # M:후문 
def preprocess_transcript(audio_file):
    transcript = openai.Audio.transcribe("whisper-1", audio_file, prompt = "서울시립대")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
                {"role": "system", "content": "너는 서울시립대학교 캠퍼스 홍보 및 길 안내 로봇이다.\
                만약 길 안내에 관한 입력값이면 처음에 'M:건물이나 장소만' 형태로 출력해. \
                만약 속도에 관한 입력값이면 'S:속도 관련 키워드만' 형태로 출력해.\
                이외의 입력값은 'Q:입력값' 형태로 그대로 출력해."},
                {"role": "user", "content": "미래관은 어디야?"},
                {"role": "assistant", "content": "M:미래관"},
                {"role": "user", "content": "속도좀 줄여줘"},
                {"role": "assistant", "content": "S:줄임"},
                {"role": "user", "content": transcript["text"]}
            ]
    )
    return response['choices'][0]['message']['content']

corrected_text = preprocess_transcript(audio_file)

print(corrected_text)

def detect_wakeup_word(audio_file):
    transcript = openai.Audio.transcribe("whisper-1", audio_file, prompt = "이봐 이루멍")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
                {"role": "system", "content": "'이봐 이루멍'이라는 wakeup-word를 인식만 해'\
                '이봐 이루멍'이라는 말이 있으면 Yes를 대답.\
                 이외의 입력값은  Ingore로 대답"},
                {"role": "user", "content": "이봐 이루멍"},
                {"role": "assistant", "content": "Yes"},
                {"role": "user", "content": "학교 좋다"},
                {"role": "assistant", "content": "Ignore"},
                {"role": "user", "content": transcript["text"]}
            ]
    )
    return response['choices'][0]['message']['content']