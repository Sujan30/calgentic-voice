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
                    "credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        
        self.service = build('calendar', 'v3', credentials=creds)
    
    def create_event(self, summary, start_time, end_time, description=None):
        """Create a calendar event"""
        try:
            event = {
                'summary': summary,
                'start': {'dateTime': start_time.isoformat()},
                'end': {'dateTime': end_time.isoformat()},
                'description': description or f"Created via SMS Calendar Assistant"
            }
            
            result = self.service.events().insert(
                calendarId='primary', 
                body=event
            ).execute()
            
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
    
    def get_upcoming_events(self, max_results=10):
        """Get upcoming calendar events"""
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []