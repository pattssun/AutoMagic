import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

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

    answer = json.loads(response.choices[0].message.content) if response.choices else "No response"

    return answer

def retrieve_pixabay_images(dict):
    """Retrieve image on Pixabay based on a query."""
    # Retrieve API key
    load_dotenv()
    pixabay_api_key = os.getenv('pixabay_api_key')
    
    # Base URL for the Pixabay API
    url = "https://pixabay.com/api/"

    # Traverse dict and retrieve image for each query
    for word, query in dict.items():
        # Parameters for the API request
        params = {
            'key': pixabay_api_key,
            'q': query[0],
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
            output_path = f"test/pixabay/{query[0]}.png"
            if data['hits']:
                image_url = data['hits'][0]['webformatURL']
                image_data = requests.get(image_url).content
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                # Save the output path to the dictionary
                dict[word].append(output_path)
        else:
            print(f"Failed to retrieve images. Status code: {response.status_code}")
            return None
        
    return dict

# Example usage
if __name__ == "__main__":
    text = "In case you find yourself in a fight, take a look at the UFC illegal moves. They're illegal because they work too well and make too much damage. Buy cheap chocolate from Costco and melt it into your own molds and sell it as homemade chocolate. Friends and family will love supporting you."
    text2 = "When buying a house, pay a bunch of crackheads to hang around the house on days of viewing to scare off potential buyers. Clean your house perfectly before the first working day of your new cleaner. When she comes, apologize for the huge mess."
    text3 = "If you want to get off of work early, take 50 milligrams of zinc on an empty stomach, you will throw up violently in five minutes. If you ever rob a bank, make sure to hold your middle finger in front of you the whole time, so the news has to blur your face in the security footage."

    # Test the image query generation and retrieval
    queries = generate_image_queries(text3)
    print(queries)
    print()
    images = retrieve_pixabay_images(queries)
    print(images)

