from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse

import logging

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

from calen import CalendarManager
from process import processText

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

@app.route('/sms', methods=['POST'])
def message():
    incoming_msg = request.form.get('Body', '').strip()
    from_number = request.form.get('From')
    
    print(f"Received SMS from {from_number}: {incoming_msg}")
    
    # Process the calendar request
    response_text = create_event(incoming_msg)
    # Send response back
    resp = MessagingResponse()
    resp.message(response_text)
    
    return str(resp)






calendar_mgr = CalendarManager()
def create_event(prompt: str):
    try:
        # Use the global calendar manager
        event_data = processText(prompt)
        
        # Debug: Check what processText returns
        print(f"processText returned: {event_data}")
        
        if event_data is None:
            return "❌ Could not parse your message. Try: 'Meeting with John tomorrow at 3pm'"
        
        if not isinstance(event_data, dict):
            return "❌ Invalid event data format"
        
        # Check required fields
        if 'summary' not in event_data or 'start' not in event_data or 'end' not in event_data:
            return "❌ Missing required event fields (summary, start, end)"
        
        result = calendar_mgr.create_event(event_data)
                
        if result:
            return f"✅ Event created: {event_data.get('summary', 'Untitled')}"
    except Exception as e:
        return "❌ Failed to create event"
        



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