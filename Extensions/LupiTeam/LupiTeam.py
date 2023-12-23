import requests
from Helpers.normalize import create_manga_overview
import json

class LupiTeam:

    base_url = "https://lupiteam.net/api"
    @staticmethod
    def SearchManga(manga_name):
        """
        Search for manga by name.

        :param manga_name: Name of the manga to search for.
        :return: JSON response from the API call if successful, None otherwise.
        """
        # Construct the URL with the manga name query
        base_url = "https://lupiteam.net/api"
        url = f"{base_url}"+"/search/"+f"{manga_name}"

        try:
            # Make a GET request to the API
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            
            # Return the JSON response if the request was successful
            raw_json=response.json()
            normalized_comics=[]
            for comic in raw_json['comics']:
                    normalized_json = create_manga_overview(
                    title=comic['title'],
                    author=comic['author'],
                    thumbnail=comic['thumbnail'],
                    status=comic['status'],
                    url=base_url + comic['url'],
                    source="LupiTeam",
                    last_chapter=base_url + comic['last_chapter']['pdf']
                    )
                    normalized_comics.append(json.loads(normalized_json))  # Convert the JSON string back to a dict
            
            return normalized_comics
        except requests.RequestException as e:
            # Handle any errors that occur during the request
            print(f"An error occurred while searching for manga: {e}")
            return None


