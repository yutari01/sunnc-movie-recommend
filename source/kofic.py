# kofic.py
import requests
import json
from api import KOBIS_API_KEY # Import the API key

def get_kofic_movie_code(title):
    """
    Searches for a movie code from KOFIC API based on the movie title.
    Args:
        title (str): The movie title to search for.
    Returns:
        str or None: Movie code (on success), or None (on failure).
    """
    if KOBIS_API_KEY == "YOUR_KOBIS_API_KEY_HERE":
        print("Warning: Please replace 'YOUR_KOBIS_API_KEY_HERE' in api.py with your actual KOBIS API Key.")
        return None

    base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest"
    search_endpoint = f"{base_url}/movie/searchMovieList.json"

    params = {
        "key": KOBIS_API_KEY,
        "movieNm": title,
        "curPage": 1,
        "itemPerPage": 1 # Get only the most accurate single result
    }

    try:
        response = requests.get(search_endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        if data and data['movieListResult'] and data['movieListResult']['movieList']:
            first_movie = data['movieListResult']['movieList'][0]
            print(f"[KOFIC] Found movie code '{first_movie['movieCd']}' for '{title}'.")
            return first_movie['movieCd']
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"[KOFIC - searchMovieList] API request error: {e}")
        return None
    except json.JSONDecodeError:
        print("[KOFIC - searchMovieList] Failed to decode JSON response.")
        return None
    except Exception as e:
        print(f"[KOFIC - searchMovieList] Unexpected error occurred: {e}")
        return None

def get_kofic_movie_details(movie_code):
    """
    Fetches detailed movie information from KOFIC API using the movie code.
    Args:
        movie_code (str): The movie code to retrieve details for.
    Returns:
        dict or None: Movie detailed information dictionary (on success), or None (on failure).
    """
    if KOBIS_API_KEY == "YOUR_KOBIS_API_KEY_HERE":
        print("Warning: Please replace 'YOUR_KOBIS_API_KEY_HERE' in api.py with your actual KOBIS API Key.")
        return None

    base_url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest"
    details_endpoint = f"{base_url}/movie/searchMovieInfo.json"

    params = {
        "key": KOBIS_API_KEY,
        "movieCd": movie_code
    }

    try:
        response = requests.get(details_endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        if data and data['movieInfoResult'] and data['movieInfoResult']['movieInfo']:
            movie_info = data['movieInfoResult']['movieInfo']

            # Extract relevant information
            directors = [d['peopleNm'] for d in movie_info.get('directors', [])]
            actors = [a['peopleNm'] for a in movie_info.get('actors', [])]
            show_types = [s['showTypeNm'] for s in movie_info.get('showTypes', [])]
            nations = [n['nationNm'] for n in movie_info.get('nations', [])]
            companies = [c['companyNm'] for c in movie_info.get('companys', [])] # 'companys' is the correct key

            return {
                "source": "KOFIC",
                "movie_code": movie_info.get('movieCd'),
                "movie_name": movie_info.get('movieNm'),
                "movie_name_eng": movie_info.get('movieNmEn'),
                "prdt_year": movie_info.get('prdtYear'),
                "open_date": movie_info.get('openDt'),
                "show_time": movie_info.get('showTm'),
                "genres": [genre['genreNm'] for genre in movie_info.get('genres', [])],
                "directors": directors,
                "actors": actors,
                "show_types": show_types,
                "nations": nations,
                "production_companies": companies,
                "audits": [audit['auditNo'] + " - " + audit['watchGradeNm'] for audit in movie_info.get('audits', [])]
            }
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"[KOFIC - searchMovieInfo] API request error: {e}")
        return None
    except json.JSONDecodeError:
        print("[KOFIC - searchMovieInfo] Failed to decode JSON response.")
        return None
    except Exception as e:
        print(f"[KOFIC - searchMovieInfo] Unexpected error occurred: {e}")
        return None

# This block is for testing this specific file directly if needed.
if __name__ == "__main__":
    test_title = "베테랑"
    code = get_kofic_movie_code(test_title)
    if code:
        info = get_kofic_movie_details(code)
        if info:
            print(f"KOFIC info for '{test_title}':")
            for key, value in info.items():
                print(f"  {key}: {value}")
        else:
            print(f"Could not retrieve KOFIC detailed info for code '{code}'.")
    else:
        print(f"Could not retrieve KOFIC code for '{test_title}'.")