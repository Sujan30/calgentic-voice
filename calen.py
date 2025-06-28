import time
import os
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class CalendarManager:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Handle authentication and build calendar service"""
        creds = None
        
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.getenv('CREDENTIALS_PATH'), self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        
        self.service = build('calendar', 'v3', credentials=creds)
    
    def create_event(self, event_data: dict):
        """Create a calendar event"""
        try:
            monterey_calendar_id = self.get_or_create_monterey_calendar()
            if not monterey_calendar_id:
                print("Failed to get or create Monterey calendar")
                return None
                
            result = self.service.events().insert(
                calendarId=monterey_calendar_id, 
                body=event_data
            ).execute()
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
    
    def get_upcoming_events(self, max_results=10):
        """Get upcoming calendar events"""
        try:
            monterey_calendar_id = self.get_or_create_monterey_calendar()
            if not monterey_calendar_id:
                print("Failed to get or create Monterey calendar")
                return []
                
            now = datetime.utcnow().isoformat() + 'Z'
            events_result = self.service.events().list(
                calendarId=monterey_calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
    
    def find_calendar_by_name(self, calendar_name: str):
        """Find calendar ID by name"""
        try:
            calendar_list = self.service.calendarList().list().execute()
            for calendar in calendar_list.get('items', []):
                if calendar.get('summary') == calendar_name:
                    return calendar.get('id')
            return None
        except HttpError as error:
            print(f"An error occurred finding calendar: {error}")
            return None
    
    def create_calendar(self, calendar_name: str):
        """Create a new calendar"""
        try:
            calendar = {
                'summary': calendar_name,
                'timeZone': 'America/Los_Angeles'
            }
            created_calendar = self.service.calendars().insert(body=calendar).execute()
            return created_calendar.get('id')
        except HttpError as error:
            print(f"An error occurred creating calendar: {error}")
            return None
    
    def share_calendar(self, calendar_id: str, email: str, role: str = 'reader'):
        """Share calendar with an email address"""
        try:
            rule = {
                'scope': {
                    'type': 'user',
                    'value': email
                },
                'role': role
            }
            created_rule = self.service.acl().insert(
                calendarId=calendar_id,
                body=rule
            ).execute()
            return created_rule
        except HttpError as error:
            print(f"An error occurred sharing calendar: {error}")
            return None
    
    def get_or_create_monterey_calendar(self):
        """Get Monterey calendar ID, create if it doesn't exist"""
        calendar_id = self.find_calendar_by_name("Monterey")
        if not calendar_id:
            calendar_id = self.create_calendar("Monterey")
            if calendar_id:
                self.share_calendar(calendar_id, "jpganoedelariva@gmail.com", "reader")
        return calendar_id
