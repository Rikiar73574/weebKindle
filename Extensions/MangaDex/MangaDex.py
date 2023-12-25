import requests
from Helpers.normalize import create_manga_overview
import json

class MangaDex:
    
    base_url = 'https://api.mangadex.org'
    @staticmethod
    def search_manga(manga_name):
        search_url = f"{MangaDex.base_url}/manga?&title={manga_name}&includedTagsMode=AND&excludedTagsMode=OR&contentRating%5B%5D=safe&contentRating%5B%5D=suggestive&contentRating%5B%5D=erotica&order%5BlatestUploadedChapter%5D=desc&includes%5B%5D=manga&includes%5B%5D=cover_art&includes%5B%5D=author&hasAvailableChapters=true"
        
        try:
            # Send a GET request to the search URL
            response = requests.get(search_url)
            
            # Check if the response status code indicates success (e.g., 200 OK)
            if response.status_code == 200:
                # Parse the response JSON content
                results = response.json()
                
                # Normalize the results with your helper function create_manga_overview
                normalized_comics=[]    
                for manga in results['data']:
                    chapt_details=MangaDex.generate_last_chapter_pdf(manga['id'])

                    
                    normalized_json = create_manga_overview(
                    title=manga['attributes']['title']['en'],
                    author=MangaDex.get_author_name_from_manga(manga['id']),
                    thumbnail=f"https://mangadex.org/covers/{manga['id']}/{MangaDex.get_cover_art_filename(manga['id'])}",
                    status=manga['attributes']['status'],
                    url=f'https://mangadex.org/title/'+manga['id'],
                    source="MangaDex",
                    last_chapter="prova"
                    )
                    normalized_comics.append(json.loads(normalized_json))
                
                
                return normalized_comics
            else:
                # Handle non-successful responses accordingly
                print(f"Error: Received a {response.status_code} status from the API.")
                return None
        except requests.exceptions.RequestException as e:
            # Handle request exceptions, such as network issues
            print(f"An error occurred: {e}")
            return None

    @staticmethod
    def generate_last_chapter_pdf(manga_id):
        """
        Static method to get manga details by manga ID from MangaDex.
        
        :param manga_id: The unique identifier for the manga on MangaDex.
        :return: A dictionary with the manga details or None if not found/error occurs.
        """
        url = f"{MangaDex.base_url}/manga/{manga_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
            manga_details = response.json()
            return manga_details
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
        return None   

    @staticmethod
    def get_author_name_from_manga(manga):
        """
        Iterates through the relationships of the manga data and extracts the name of the author.
        
        :param manga: A dictionary representing the manga data, which includes 'relationships'.
        :return: The name of the author, or None if not found.
        """

        # Check if 'relationships' key exists in the manga record
        if 'relationships' in manga:
            # Iterate over each relationship
            for relationship in manga['relationships']:
                # Check if the relationship type is 'author' and it has 'attributes'
                if relationship.get('type') == 'author' and 'attributes' in relationship:
                    # Return the author's name if found
                    return relationship['attributes'].get('name', None)

        # Return None if no author type or name was found
        return None

    @staticmethod
    def get_cover_art_filename(manga):
        """
        Iterates through the relationships of the manga data and extracts the file name of the cover art.
        
        :param manga: A dictionary representing the manga data, which includes 'relationships'.
        :return: The file name of the cover art, or None if not found.
        """

        # Check if 'relationships' key exists in the manga record
        if 'relationships' in manga:
            # Iterate over each relationship
            for relationship in manga['relationships']:
                # Check if the relationship type is 'cover_art' and it has 'attributes'
                if relationship.get('type') == 'cover_art' and 'attributes' in relationship:
                    # Return the cover art's file name if found
                    return relationship['attributes'].get('fileName', None)

        # Return None if there's no cover_art type or fileName was found
        return None


