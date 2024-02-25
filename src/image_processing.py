import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from src.text_processing import read_text_file, read_text_file_by_line

def generate_image_queries(text):
    load_dotenv()
    client = OpenAI(api_key=os.getenv('openai_api_key'))

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",  
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "Analyze a TikTok video transcript to pinpoint essential single-word keywords. For each, craft a specific Pixabay search query to visually enrich the video. Ensure these queries are brief yet effective, aiming for a diverse and visually stimulating presentation. Output a list of dictionaries in JSON, each containing 'keyword' and 'query', under the key 'queries'. Prioritize unique keywords for a dynamic image sequence to boost viewer engagement. Utilize Pixabay's wide image selection for optimal results."},
            {"role": "user", "content": "Provide a list of search queries for the following transcription text input: " + text},
        ]
    )

    answer = json.loads(response.choices[0].message.content) if response.choices else "No response"

    return answer['queries']

def generate_all_image_queries(body_text_chunks):
    all_queries = []
    
    for chunk in body_text_chunks:
        queries = generate_image_queries(chunk)
        all_queries += queries

    return all_queries

def retrieve_pixabay_images(queries):
    """Retrieve image on Pixabay based on a query."""
    # Retrieve API key
    load_dotenv()
    pixabay_api_key = os.getenv('pixabay_api_key')
    
    # Base URL for the Pixabay API
    url = "https://pixabay.com/api/"

    # Traverse dict and retrieve image for each query
    for query in queries:
        # Parameters for the API request
        params = {
            'key': pixabay_api_key,
            'q': query['query'],
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
            output_path = f"test/pixabay/{query['query']}.png"
            if data['hits']:
                image_url = data['hits'][0]['webformatURL']
                image_data = requests.get(image_url).content
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                # Save the output path to the dictionary
                query['image_path'] = output_path
        # If the request was not successful, set the image path to None
        if 'image_path' not in query:
            query['image_path'] = None
        
    return queries

# Example usage
if __name__ == "__main__":
    text = "In case you find yourself in a fight, take a look at the UFC illegal moves. They're illegal because they work too well and make too much damage."
    text2 = "When buying a house, pay a bunch of crackheads to hang around the house on days of viewing to scare off potential buyers. Clean your house perfectly before the first working day of your new cleaner. When she comes, apologize for the huge mess."
    text3 = "If you want to get off of work early, take 50 milligrams of zinc on an empty stomach, you will throw up violently in five minutes. If you ever rob a bank, make sure to hold your middle finger in front of you the whole time, so the news has to blur your face in the security footage."
    body_text = read_text_file("test/tiktok.txt")
    body_text_chunks = read_text_file_by_line("test/tiktok.txt")

    # Test the image query generation and retrieval
    queries = generate_all_image_queries(body_text_chunks)
    print(queries)
    print()
    print(f"Queries generated: {len(queries)}")
    images = retrieve_pixabay_images(queries)
    print()
    print(images)