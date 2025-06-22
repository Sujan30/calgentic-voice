from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse

import logging

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

from calen import CalendarManager
from process import processText


@app.route('/sms', methods=['POST'])
def message():
    incoming_msg = request.form.get('Body', '').strip()
    from_number = request.form.get('From')
    
    print(f"Received SMS from {from_number}: {incoming_msg}")
    
    # Process the calendar request
    response_text = 'yo'
    
    # Send response back
    resp = MessagingResponse()
    resp.message(response_text)
    
    return str(resp)


@app.route('/voice', methods=['GET', 'POST'])
def voice():
    print(f"=== WEBHOOK RECEIVED ===")
    print(f"Method: {request.method}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Form: {dict(request.form)}")
    print(f"Args: {dict(request.args)}")

    if request.method == 'GET':
        return "Webhook endpoint is working!"
    
    print("Voice webhook received!")
    response = VoiceResponse()
    response.say('Hello Sujan!')
    response.record(
        action='/process-recording',
        max_length=30,
        finish_on_key='#',
        play_beep=True
    )
    response.say("I didn't hear anything. Please try calling again.")
    return str(response)



calendar_mgr = CalendarManager()

@app.route('/create-event', methods=['POST'])
def create_event():
    try:
        data = request.json()
        if not data:
            return {
                "error processing request"
            }
        prompt = data['prompt']
        event_data = processText(prompt)
        if calendar_mgr.create_event(event_data):
            return "event created"
        else:
            return 'failed to create event'
    except Exception as e:
        print(f'{e}')




@app.route('/process-recording', methods=['POST'])
def process_recording():
    print("Recording webhook received!")
    recording_url = request.form.get('RecordingUrl')
    print(f"Recording URL: {recording_url}")
    
    response = VoiceResponse()
    response.say("Thanks for the call!")
    response.hangup()
    return str(response)

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')