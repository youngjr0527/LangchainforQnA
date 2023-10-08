# LangchainforQnA

## 소개

`LangchainforQnA`는 Langchain을 이용하여 실시간 음성 인식과 텍스트 음성 변환, 그리고 질문 응답을 위한 챗봇 기능을 통합하는 프로젝트이다. 이 프로젝트는 OpenAI의 Whisper STT API, 네이버의 TTS API, 그리고 LLM 모델인 GPT-3.5-turbo를 사용한다.

## 주요 기능

1. **실시간 음성 인식**: OpenAI의 Whisper API를 사용하여 실시간으로 음성을 인식한다.
2. **텍스트 음성 변환**: 네이버의 Voice TTS API를 사용하여 텍스트를 음성으로 변환한다.
3. **질문 응답 챗봇**: GPT-3.5-turbo를 사용하여 사용자의 질문에 답한다.

## 설치 방법

```bash
pip install -r requirements.txt
```

## 주요 파일 설명

- `main.py`: 프로그램의 메인 실행 함수
- `whisper_STT.py`: 실시간 음성 인식을 위한 클래스 정의
- `Naver_TTS.py`: 텍스트를 음성으로 변환하는 클래스 정의

  
## 사용 방법

1. `main.py` 스크립트를 실행하여 프로그램을 시작한다.
2. 호출명령어('헬로 이루멍')를 오디오 출력 장치에 전달한다.
3. 호출명령어가 인식되면 다음과 같은 작업(Task)을 음성으로 지시할 수 있다.
    - 목적지까지의 경로 안내
    - 로봇의 이동 속도 조절(가속, 감속)
    - 학교 관련 정보 질문 및 조회



