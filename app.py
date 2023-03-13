from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Set the API endpoint and the API key
endpoint = 'https://api.remove.bg/v1.0/removebg'
api_key = 'ekz5gjB1vnd6REFibrBbnoMD'

# Route to Twilio services
@app.route('/sms', methods=['POST'])
def sms():
    # Get the incoming message from Twilio
    message = request.form['Body']
    
    # Remove the background from the image using remove.bg API
    response = requests.post(
        endpoint,
        headers={'X-Api-Key': api_key},
        files={'image_url': message},
        data={'size': 'auto'}
    )
    
    # Send the image to the user using Twilio
    resp = MessagingResponse()
    resp.message().media(response.content)
    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)

