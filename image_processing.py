import requests
import os
from dotenv import load_dotenv

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
    query = "friends and family"
    images = retrieve_pixabay_image(query, f"resources/images/{query}.png")
    
    # Check if the image was saved
    if os.path.exists(f"resources/images/{query}.png"):
        print(f"\nImage saved at resources/images/{query}.png\n")
    else:
        print("Image not saved")
