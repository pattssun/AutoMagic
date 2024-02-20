import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

def generate_image_queries(text):
    load_dotenv()
    client = OpenAI(api_key=os.getenv('openai_api_key'))

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",  
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to transform a TikTok video transcription to identify pivotal words and their corresponding Pixabay search queries. Segment the transcription into distinct thematic sections, pinpointing a key word or phrase from each segment. For each key word, craft a 1-3 word search query that encapsulates its essence. These queries will direct the image selection to visually complement the video's narrative. Consider Pixabay's limitations for niche topics and aim for queries with broad image availability. Output the key words with their queries in JSON format as {original_word: query}. This structured output will facilitate synchronizing the retrieved images with their respective segments in the video, based on the original word's timestamp."},
            {"role": "user", "content": "Provide a list of search queries for the following transcription text input: " + text},
        ]
    )

    answer = response.choices[0].message.content if response.choices else "No response"

    return answer

def retrieve_pixabay_image(query, output_path):
    """Retrieve image on Pixabay based on a query."""
    # Retrieve API key
    load_dotenv()
    pixabay_api_key = os.getenv('pixabay_api_key')
    
    # Base URL for the Pixabay API
    url = "https://pixabay.com/api/"
    
    # Parameters for the API request
    params = {
        'key': pixabay_api_key,
        'q': query,
        'image_type': 'photo',
        'orientation': 'horizontal'
    }
    
    # Make the GET request to the Pixabay API
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Save first image from the URL as a PNG file
        if data['hits']:
            image_url = data['hits'][0]['webformatURL']
            image_data = requests.get(image_url).content
            with open(output_path, 'wb') as f:
                f.write(image_data)
    else:
        print(f"Failed to retrieve images. Status code: {response.status_code}")
        return None

# Example usage
if __name__ == "__main__":
    # query = "security footage"
    # images = retrieve_pixabay_image(query, f"resources/images/{query}.png")
    
    # # Check if the image was saved
    # if os.path.exists(f"resources/images/{query}.png"):
    #     print(f"\nImage saved at resources/images/{query}.png\n")
    # else:
    #     print("Image not saved")

    text = "When buying a house, pay a bunch of crackheads to hang around the house on days of viewing to scare off potential buyers. Clean your house perfectly before the first working day of your new cleaner. When she comes, apologize for the huge mess."
    queries = generate_image_queries(text)
    print(queries)
