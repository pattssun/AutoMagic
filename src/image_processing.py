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
            {"role": "system", "content": "You are a helpful assistant designed to transform a TikTok transcript by identifying key words or phrases for dynamic visual content. Create concise, 1-2 word search queries for each key term to find relevant Pixabay images. Aim for a varied and engaging visual flow, leveraging Pixabay's extensive library. Consider the broadness of Pixabay's image repository to maximize your query's potential. Output queries in JSON as {original_word: [query]}, ensuring unique keys and frequent image updates to enhance the video narrative."},
            {"role": "user", "content": "Provide a list of search queries for the following transcription text input: " + text},
        ]
    )

    answer = response.choices[0].message.content if response.choices else "No response"

    return answer

########### STUCK HERE ############
def retrieve_pixabay_image(query, dict):
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
        output_path = f"test/pixabay_images/{query}.png"
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
