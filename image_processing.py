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
            {"role": "system", "content": "You are a helpful assistant designed to engage your audience with dynamic visual content by dissecting the TikTok video transcription into finer thematic segments. Focus on extracting multiple pivotal words or phrases throughout the transcript. For each extracted word, devise a concise, 1-2 word search query that accurately represents its theme or subject matter. These refined queries will guide the selection of a diverse array of images from Pixabay, ensuring a visually rich and engaging video experience. Consider the broadness of Pixabay's image repository to maximize your query's potential. Format the output in JSON format as {original_word: query}, aiming for a higher frequency of image changes throughout the video. This approach will keep the audience captivated by closely aligning the visual transitions with the video's evolving narrative, based on the timestamps of the original words."},
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
    text2 = "In case you find yourself in a fight, take a look at the UFC illegal moves. They're illegal because they work too well and make too much damage. Buy cheap chocolate from Costco and melt it into your own molds and sell it as homemade chocolate. Friends and family will love supporting you."
    queries = generate_image_queries(text2)
    print(queries)
