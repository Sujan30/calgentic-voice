from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv('GEMINI_API_KEY')
)


def processText(text: str):
    response = client.models.generate_content(
    model="gemini-2.0-flash-lite",
    contents=[
        """Your goal is to take the users text and turn it into a json format like this:
        event = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-05-28T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2015-05-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
} Only return the information in json format and nothing else, like legit nothing else.  
        """,
        [f'here is the users query: {text}']
    ]
  
)
    return response.text.replace('json','').replace('```','')

event_data = processText('I have a meeting tomorrow at 3pm')



