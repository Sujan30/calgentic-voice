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
        
        
        await page.locator("#wednesday-august-14").scroll_into_view_if_needed()
        
        
        events = await page.locator("#wednesday-august-14 ~ ul.wp-block-list li").all()
        
        results = []
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
            
            results.append({
                "time": time_part,
                "name": event_name,
                "description": description
            })
        
        await browser.close()
        return results

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
    