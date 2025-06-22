from twilio.rest import Client
import os
from dotenv import load_dotenv
import time

load_dotenv()

account_sid = os.getenv('TWILLIO_ACCOUNT_SID')
auth_token = os.getenv('TWILLIO_AUTH_TOKEN')
number = os.getenv('TWILLIO_NUMBER')
my_number = os.getenv('MY_NUMBER')

try:
    client = Client(account_sid, auth_token)
    
    for i in range(3):
        print(f"Test call {i+1}...")
    
        call = client.calls.create(
        from_=number,
        to=my_number,
        url='https://4b13-50-209-173-229.ngrok-free.app/voice', 
        caller_id=my_number
        )
    
        time.sleep(10)
        call_details = client.calls(call.sid).fetch()
        print(f"Call {i+1} status: {call_details.status}")
        time.sleep(10)

    message = client.messages.create(
    body="Calendar Assistant: Reply with your event details",
    from_=number,
    to=my_number
)
    print(f'message sid: {message.sid}')
    
    print(f"Call SID: {call.sid}")
    
    # Wait a bit for the call to process
    time.sleep(5)
    
    call_details = client.calls(call.sid).fetch()
    print(f"Call Status: {call_details.status}")
    print(f"Call Direction: {call_details.direction}")
    
    if call_details.status == 'failed':
        print(f"Error Message: {call_details.Status}")
        
except Exception as e:
    print(f'Error: {e}')