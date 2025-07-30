# query.py
import datetime
# source 디렉토리 내의 모듈에서 함수들을 임포트합니다.
from source.tmdb import get_tmdb_movie_info
from source.kofic import get_kofic_movie_code, get_kofic_movie_details

def display_combined_movie_info(combined_data, query_title):
    """
    TMDB와 KOFIC에서 합쳐진 영화 정보를 보기 좋게 출력합니다.

    Args:
        combined_data (dict): TMDB와 KOFIC 정보가 통합된 딕셔너리.
        query_title (str): 사용자가 검색한 원본 영화 제목.
    """
    print("\n" + "="*40)
    print(f"'{query_title}' 통합 검색 결과")
    print("="*40 + "\n")

    if not combined_data:
        print(f"'{query_title}'에 대한 어떤 정보도 찾을 수 없습니다.")
        return

    # 공통 정보 출력
    print(f"** 영화 제목 (국문): {combined_data.get('movie_name_kr', '정보 없음')} **")
    print(f"** 영화 제목 (영문): {combined_data.get('movie_name_en', '정보 없음')} **")
    print(f"제작 연도: {combined_data.get('prdt_year', '정보 없음')}")
    print(f"한국 개봉일: {combined_data.get('release_date_kr', '정보 없음')}")
    print(f"상영 시간: {combined_data.get('runtime', '정보 없음')}분")
    print(f"평점: {combined_data.get('vote_average', '정보 없음')}/10 (TMDB)")

    genres = combined_data.get('genres', [])
    if genres:
        print(f"장르: {', '.join(genres)}")

    directors = combined_data.get('directors', [])
    if directors:
        print(f"감독: {', '.join(directors)}")

    actors = combined_data.get('actors', [])
    if actors:
        # 주요 출연진은 최대 5명만 보여주고 나머지는 ...으로 처리
        actors_display = ', '.join(actors[:5])
        if len(actors) > 5:
            actors_display += "..."
        print(f"주요 출연진: {actors_display}")

    print(f"제작 국가: {', '.join(combined_data.get('nations', []))}")
    print(f"영화 형태: {', '.join(combined_data.get('show_types', []))}")
    print(f"제작/배급사: {', '.join(combined_data.get('production_companies', []))}")
    print(f"심의 등급: {', '.join(combined_data.get('audits', []))}")

    print("\n--- 줄거리/개요 ---")
    overview = combined_data.get('overview', '정보 없음')
    if overview != '정보 없음':
        print(overview)
    else:
        print("줄거리/개요 정보가 없습니다.")

    print("\n--- 추가 정보 ---")
    tagline = combined_data.get('tagline', '정보 없음')
    if tagline != '정보 없음':
        print(f"슬로건/태그라인: {tagline}")

    if combined_data.get('poster_path'):
        print(f"포스터 URL: {combined_data.get('poster_path')}")
    if combined_data.get('backdrop_path'):
        print(f"배경 이미지 URL: {combined_data.get('backdrop_path')}")

    print("\n" + "="*40 + "\n")


if __name__ == "__main__":
    while True:
        movie_title_query = input("검색할 영화 제목을 입력하세요 (종료하려면 'q' 입력): ").strip()

        if movie_title_query.lower() == 'q':
            print("프로그램을 종료합니다.")
            break

        if not movie_title_query:
            print("영화 제목을 입력해주세요.")
            continue

        print(f"\n'{movie_title_query}'에 대한 정보 검색 중...")

        tmdb_info = get_tmdb_movie_info(movie_title_query)
        kofic_info = None
        kofic_movie_code = get_kofic_movie_code(movie_title_query)

        if kofic_movie_code:
            kofic_info = get_kofic_movie_details(kofic_movie_code)

        combined_info = {}

        # TMDB 정보 합치기
        if tmdb_info:
            combined_info['movie_name_kr'] = tmdb_info.get('title')
            combined_info['movie_name_en'] = tmdb_info.get('original_title')
            combined_info['overview'] = tmdb_info.get('overview')
            combined_info['release_date_kr'] = tmdb_info.get('release_date')
            combined_info['vote_average'] = tmdb_info.get('vote_average')
            combined_info['runtime'] = tmdb_info.get('runtime')
            combined_info['poster_path'] = tmdb_info.get('poster_path')
            combined_info['backdrop_path'] = tmdb_info.get('backdrop_path')
            combined_info['tagline'] = tmdb_info.get('tagline')
            combined_info['genres'] = tmdb_info.get('genres', []) # TMDB 장르 우선

        # KOFIC 정보 합치기 (중복되는 정보는 TMDB 것으로 유지하고, 없는 정보만 추가)
        if kofic_info:
            if 'movie_name_kr' not in combined_info or not combined_info['movie_name_kr']:
                 combined_info['movie_name_kr'] = kofic_info.get('movie_name')
            if 'movie_name_en' not in combined_info or not combined_info['movie_name_en']:
                 combined_info['movie_name_en'] = kofic_info.get('movie_name_eng')

            # KOFIC의 개봉일이 더 정확한 한국 개봉일일 수 있으므로 우선 순위 부여
            combined_info['release_date_kr'] = kofic_info.get('open_date', combined_info.get('release_date_kr'))
            # KOFIC의 상영시간도 정확할 수 있음
            combined_info['runtime'] = kofic_info.get('show_time', combined_info.get('runtime'))
            
            # KOFIC에만 있는 정보는 추가
            combined_info['prdt_year'] = kofic_info.get('prdt_year')
            
            # 장르 병합 (중복 제거)
            kofic_genres = kofic_info.get('genres', [])
            if kofic_genres:
                if 'genres' in combined_info:
                    combined_info['genres'] = list(set(combined_info['genres'] + kofic_genres))
                else:
                    combined_info['genres'] = kofic_genres

            combined_info['directors'] = kofic_info.get('directors', [])
            combined_info['actors'] = kofic_info.get('actors', [])
            combined_info['show_types'] = kofic_info.get('show_types', [])
            combined_info['nations'] = kofic_info.get('nations', [])
            combined_info['production_companies'] = kofic_info.get('production_companies', [])
            combined_info['audits'] = kofic_info.get('audits', [])

        display_combined_movie_info(combined_info, movie_title_query)