from calen import CalendarManager
import json

def processOutput(events):
  if isinstance(events, str):
        events = json.loads(events)
  
  event_data = []
  for event in events:
        event_data.append(add_relevant_info(event))
  
  return event_data #all the info formatted well


def createEvents(event_data):
      cal = CalendarManager()
      for event in event_data:
            try:
                cal.create_event(event)
                
            except Exception as e:
                print(f'error adding event {e}')
    
          

def add_relevant_info(event):
    from datetime import datetime, timedelta
    
    # Handle null end_time
    start_time = event['start_time']
    end_time = event['end_time']
    
    if end_time is None:
        # Parse start time and add 1 hour
        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_dt = start_dt + timedelta(hours=1)
        end_time = end_dt.isoformat()

    event_data = {
  'summary': event['name'],
  'location': '',
  'description': event['description'],
  'start': {
    'dateTime': event['start_time'],
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': event['end_time'],
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'lpage@example.com'} #to do: Add jasons email
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
    return event_data
  