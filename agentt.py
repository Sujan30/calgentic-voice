from dotenv import load_dotenv
import os
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_KEY'),
    
)


def processInfo(event: json):
    response = client.responses.create(
        model='gpt-4o-mini', 
        instructions="""
            
                "You are a data cleaning assistant. Clean and convert the following messy car event data into structured JSON. "
                "For each object, return a new object with the following fields:\n\n"
                "1. 'name': event name\n"
                "2. 'start_time': full ISO 8601 datetime in format 'YYYY-MM-DDTHH:MM:SS-07:00'\n"
                "3. 'end_time': same ISO 8601 format, or null if not provided\n"
                "4. 'description': cleaned version with extra symbols (e.g., \\xa0) removed\n\n"
                "Start the first event on '2025-08-12' and increment the date when the group of events changes to the next day. "
                "Use the day information from the scraped data to assign correct dates from 2025-08-12 through 2025-08-17. "
                "Use timezone offset -07:00 for all events. Normalize AM/PM time to 24-hour clock in ISO format. "
                "If only one time is given, treat it as 'start_time' and set 'end_time' to null."
                "Return only the JSON, don't return anything else. No other text should be there."
            """
        ,
        input=f"Here is the event data: ```{json.dumps(event)}```"
        
    ,
    temperature=0.2
)
    output = response.output_text.replace('json','').replace('```','') #stripping all the other uneccessary stuff
    print(f'token usage: {response.usage.total_tokens}')
    return output  

    


