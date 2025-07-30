# tmdb.py
import requests
import json
from api import TMDB_API_KEY # Import the API key

def get_tmdb_movie_info(title):
    """
    Fetches movie information from TMDB based on the movie title.
    Args:
        title (str): The movie title to search for.
    Returns:
        dict or None: A dictionary containing movie information (on success), or None (on failure).
    """
    if TMDB_API_KEY == "YOUR_TMDB_API_KEY_HERE":
        print("Warning: Please replace 'YOUR_TMDB_API_KEY_HERE' in api.py with your actual TMDB API Key.")
        return None

    base_url = "https://api.themoviedb.org/3"
    search_endpoint = f"{base_url}/search/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "ko-KR" # Request Korean information (optional)
    }

    try:
        response = requests.get(search_endpoint, params=params)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()

        if data and data['results']:
            # Return the first, most relevant result
            first_result = data['results'][0]
            movie_id = first_result['id']

            # Get detailed information using the movie ID
            details_endpoint = f"{base_url}/movie/{movie_id}"
            details_params = {
                "api_key": TMDB_API_KEY,
                "language": "ko-KR"
            }
            details_response = requests.get(details_endpoint, params=details_params)
            details_response.raise_for_status()
            details_data = details_response.json()

            return {
                "source": "TMDB",
                "id": details_data.get('id'),
                "title": details_data.get('title'),
                "original_title": details_data.get('original_title'),
                "overview": details_data.get('overview'),
                "release_date": details_data.get('release_date'),
                "vote_average": details_data.get('vote_average'),
                "genres": [genre['name'] for genre in details_data.get('genres', [])],
                "poster_path": f"https://image.tmdb.org/t/p/w500{details_data.get('poster_path')}" if details_data.get('poster_path') else None,
                "backdrop_path": f"https://image.tmdb.org/t/p/w1280{details_data.get('backdrop_path')}" if details_data.get('backdrop_path') else None,
                "tagline": details_data.get('tagline'),
                "runtime": details_data.get('runtime')
            }
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"[TMDB] API request error: {e}")
        return None
    except json.JSONDecodeError:
        print("[TMDB] Failed to decode JSON response.")
        return None
    except Exception as e:
        print(f"[TMDB] Unexpected error occurred: {e}")
        return None

# This block is for testing this specific file directly if needed.
if __name__ == "__main__":
    test_title = "이터널스"
    info = get_tmdb_movie_info(test_title)
    if info:
        print(f"TMDB info for '{test_title}':")
        for key, value in info.items():
            print(f"  {key}: {value}")
    else:
        print(f"Could not retrieve TMDB info for '{test_title}'.")