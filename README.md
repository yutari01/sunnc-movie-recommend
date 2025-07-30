-----

# Sunny C Movie Recommend

이 프로젝트는 TMDb (The Movie Database)와 영화진흥위원회(KOFIC)에서 영화 정보를 자동으로 수집하고 통합하여 사용자에게 제공하는 Python 기반의 솔루션입니다. 영화 제목을 입력하면 다양한 출처의 상세한 정보를 한눈에 확인할 수 있습니다.

## 🚀 주요 기능

  * **TMDb (The Movie Database) 연동**: 영화의 기본 정보 (제목, 영문 제목, 개요, 개봉일, 평점, 장르, 러닝타임, 포스터/배경 이미지, 슬로건)를 가져옵니다.
  * **영화진흥위원회 (KOFIC) 연동**: 한국 영화에 특화된 정보 (국문/영문 영화명, 제작 연도, 한국 개봉일, 상영 시간, 감독, 주요 출연진, 영화 형태, 제작 국가, 제작/배급사, 심의 등급)를 가져옵니다.
  * **통합 정보 제공**: TMDb와 KOFIC에서 수집된 모든 정보를 합쳐서 사용자에게 보기 좋게 정리하여 출력합니다.
  * **모듈화된 코드**: 각 API 연동 로직은 별도의 파일로 분리되어 코드의 가독성과 유지보수성을 높였습니다. API 키는 별도 파일에서 관리됩니다.

## 📁 프로젝트 구조

```
your_project_name/
├── api_sample.py             # API 키를 저장하는 샘플 파일 (실제 사용 시 api.py로 복사 및 키 입력)
├── query.py                  # 메인 실행 파일: 사용자 입력, API 호출 조율, 결과 통합 출력
└── source/                   # API 연동 로직이 담긴 모듈
    ├── tmdb.py               # TMDb API 호출 함수
    └── kofic.py              # KOFIC API 호출 함수
```

## ⚙️ 설치 및 설정

이 프로젝트를 실행하기 위해 다음 단계를 따르세요.

### 1\. Python 및 `pip` 설치

Python 3.8 이상 버전이 설치되어 있어야 합니다.

### 2\. 필요한 라이브러리 설치

프로젝트 루트 디렉토리에서 다음 명령어를 실행하여 필요한 Python 라이브러리들을 설치합니다:

```bash
pip install requests
```

### 3\. API 키 설정

TMDb, KOFIC API를 사용하기 위해 발급받은 API 키를 설정해야 합니다.

1.  **`api_sample.py` 파일 복사 및 이름 변경**:
    `api_sample.py` 파일 이름을 `api.py`로 변경합니다.

2.  **API 키 입력**:
    복사한 `api.py` 파일을 열고, 아래 변수에 발급받은 실제 API 키를 입력합니다.

    ```python
    # api.py
    TMDB_API_KEY = "YOUR_TMDB_API_KEY_HERE"
    KOBIS_API_KEY = "YOUR_KOBIS_API_KEY_HERE"
    ```

      * **TMDb API 키 발급**: [https://www.themoviedb.org/documentation/api](https://www.themoviedb.org/documentation/api)
      * **KOFIC API 키 발급**: [http://www.kobis.or.kr/kobisopenapi/homepg/main/main.do](http://www.kobis.or.kr/kobisopenapi/homepg/main/main.do)

    **경고**: `api.py` 파일은 `.gitignore`에 추가하여 **절대 GitHub와 같은 공개 저장소에 업로드하지 마세요.** API 키가 노출되면 무단 사용될 위험이 있습니다.

## 🚀 사용 방법

모든 설정이 완료되었다면, 프로젝트의 루트 디렉토리에서 다음 명령어를 실행하여 프로그램을 시작할 수 있습니다:

```bash
python query.py
```

프로그램이 시작되면 영화 제목을 입력하라는 메시지가 표시됩니다.

```
검색할 영화 제목을 입력하세요 (종료하려면 'q' 입력):
```

여기에 검색하고자 하는 영화 제목을 입력하고 Enter를 누르면, TMDb와 KOFIC에서 수집된 통합 정보가 터미널에 출력됩니다. 프로그램을 종료하려면 `q`를 입력하세요.

-----