from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

from flask import Flask, request, redirect

app = Flask(__name__)

# Set the API endpoint and the API key
endpoint = 'https://api.remove.bg/v1.0/removebg'
api_key = 'ekz5gjB1vnd6REFibrBbnoMD'

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Get the incoming message
    incoming_msg = request.values.get('Body', '').strip()
    # Get the media URL from the message
    media_url = request.values.get('MediaUrl0', '')
    # Check if the message has media
    if media_url:
        # Download the image
        response = requests.get(media_url)
        img = response.content
        # Set up the API headers and parameters
        headers = {'X-Api-Key': api_key}
        files = {'image_file': img}
        params = {'size': 'auto'}
        # Send a POST request to Remove.bg API to remove the background
        response = requests.post(endpoint, headers=headers, files=files, params=params)
        # Save the resulting image in JPEG format
        with open('result.jpg', 'wb') as out:
            out.write(response.content)
        # Send the resulting image back to the user
        resp = MessagingResponse()
        message = resp.message()
        message.media('http://{}/result.jpg'.format(request.host))
        return str(resp)
    else:
        # Send a default message if no media is found
        resp = MessagingResponse()
        resp.message("Send me an image with a background to remove it!")
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

