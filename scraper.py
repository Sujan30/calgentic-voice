from playwright.async_api import async_playwright
import asyncio

import json

from agentt import processInfo

from process import processOutput, createEvents

async def scrape_monterey_events():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.seemonterey.com/monterey-car-week-events-by-day/")
        
        target_days = [
            "Tuesday, August 12",
            "Wednesday, August 13", 
            "Thursday, August 14",
            "Friday, August 15",
            "Saturday, August 16",
            "Sunday, August 17"
        ]
        
        all_results = []
        for day in target_days:
            day_header = page.locator(f"h3:has-text('{day}')")
            if await day_header.count() > 0:
                # Get the UL element that follows this header
                events_list = day_header.locator("+ ul")
                if await events_list.count() > 0:
                    events = await events_list.locator("li").all()
                    
                    for event in events:
                        # Get the full text content
                        full_text = await event.inner_text()
                        
                        # Extract time (before the first comma)
                        time_part = full_text.split(',')[0].strip()
                        
                        # Extract event name (from the link)
                        event_link = event.locator("a[data-type='event']")
                        event_name = await event_link.inner_text() if await event_link.count() > 0 else "No name"
                        
                        # Extract description (after the colon and dash)
                        description = full_text.split(' - ', 1)[1] if ' - ' in full_text else ""
                        
                        all_results.append({
                            "time": time_part,
                            "name": event_name,
                            "description": description,
                            "day": day
                        })
        
        await browser.close()
        return all_results

async def main():
    """events = await scrape_monterey_events()
    print(f'raw events: \n{events}')
    with open('monterey_events.json', 'w') as f:
        f.write(json.dumps(events, indent=2))
    """
    with open('monterey_events.json') as f:
        events = f.read()
    
    new_events=processInfo(events)

    event_data = processOutput(new_events)

    createEvents(event_data=event_data)
    
    print(f'processed events: {new_events}')
    return new_events

# Run it
asyncio.run(main())
    