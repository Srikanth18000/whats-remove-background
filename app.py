import os
from twilio.twiml.messaging_response import MessagingResponse
from removebg import RemoveBg

# Set up the Remove.bg API client
removebg = RemoveBg(api_key, 'error')

def remove_background(image_url):
    # Remove the background from the image
    response = removebg.remove_background_from_url(image_url)

    # Save the result to a file
    with open('output.png', 'wb') as f:
        f.write(response.content)

    return 'output.png'

def handle_message(message):
    # Check if the message has any image attachments
    if 'MediaUrl0' in message:
        image_url = message['MediaUrl0']
        image_path = remove_background(image_url)

        # Create a Twilio messaging response with the processed image attached
        resp = MessagingResponse()
        resp.message().media(image_path)

        return str(resp)
    else:
        # If the message doesn't have any image attachments, just send a reply
        return 'Send me an image and I will remove the background!'

if __name__ == '__main__':
    from flask import Flask, request

    app = Flask(__name__)

    @app.route('/sms', methods=['POST'])
    def webhook():
        message = request.form

        response = handle_message(message)

        return response

    if __name__ == '__main__':
        app.run(debug=True)

