import requests
import json

# Define parameters for the Sightengine API request
params = {
    'models': 'nudity-2.0,wad,offensive,faces,text-content,gore,tobacco,genai,gambling',
    'api_user': '342655828',
    'api_secret': 'ND6AbWEfkJNE7qSkRcFYJRud5KbPFTKo'
}

# Specify the file path of the image you want to analyze
image_path = r"C:\Users\Afnan\Downloads\dg.webp"

# Open the image file in binary mode
with open(image_path, 'rb') as file:
    files = {'media': file}

    # Send a POST request to the Sightengine API
    response = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        output = json.loads(response.text)

        # Print the full response
        print("Response from Sightengine API:")
        print(json.dumps(output, indent=4))

        # Check for nudity detection
        nudity = output["nudity"]
        if nudity.get("raw") is not None and nudity["raw"] > 0.5:
            print("Nudity detected:", "{:.0%}".format(nudity["raw"]))

        # Check for offensive content detection
        offensive = output["offensive"]
        if offensive.get("prob") is not None and offensive["prob"] > 0.5:
            print("Offensive content detected:", "{:.0%}".format(offensive["prob"]))

        # Check for other detected content
        # Add more fields as needed

    else:
        print("Error:", response.text)
