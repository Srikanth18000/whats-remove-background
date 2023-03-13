from flask import Flask, request, jsonify, make_response
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
    error_message = {"errors":[{"title":"No image given","code":"missing_source","detail":"Please provide the source image in the image_url, image_file or image_file_b64 parameter."}]}
    response = make_response(jsonify(error_message), 400)
    response.headers['Content-Type'] = 'application/json'

    resp = messaging_response.Message()
    resp.body('Error: ' + response.get_data().decode('utf-8'))
    resp.content_type = 'application/json'
    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)

