from calen import CalendarManager
import json
import re

def processOutput(events):
  if isinstance(events, str):
        events = json.loads(events)
  
  event_data = []
  for event in events:
        event_data.append(add_relevant_info(event))
  
  return event_data #all the info formatted well


def extract_address(description: str) -> str:
    """Extract address/location from event description"""
    if not description:
        return ""
    
    location_patterns = [
        r'downtown\s+(Carmel[^,]*)',
        r'(WeatherTech Raceway[^,]*)',
        r'(Laguna Seca[^,]*)',
        r'(Pebble Beach[^,]*)',
        r'(Carmel-by-the-Sea|Carmel by-the-Sea)',
        r'(Monterey[^,]*)',
        r'(Pacific Grove[^,]*)',
        r'at\s+([^,]+(?:Avenue|Ave|Street|St|Road|Rd|Drive|Dr|Boulevard|Blvd|Way|Lane|Ln)[^,]*)',
        r'on\s+([^,]+(?:Avenue|Ave|Street|St)[^,]*)',
        r'(Golf Links[^,]*)',
        r'(Ocean Ave[^,]*)',
        r'(Alvarado St[^,]*)'
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, description, re.IGNORECASE)
        if match:
            location = match.group(1).strip()
            location = re.sub(r'^(at|on|in)\s+', '', location, flags=re.IGNORECASE)
            location = re.sub(r'\s*\([^)]*\).*$', '', location)  # Remove parenthetical content
            location = re.sub(r'\s*:.*$', '', location)  # Remove content after colon
            return location.strip()
    
    return ""

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
  'location': extract_address(event['description']),
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
    {'email': 'jpganoedelariva@gmail.com'}
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

def processText(prompt: str):
    """Simple text processing for voice/SMS interface"""
    return None
  