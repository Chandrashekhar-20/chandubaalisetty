import json
from datetime import datetime
from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Open the website
    page.goto("https://www.budgetticket.in/")

    # Select origin and destination
    page.get_by_role("textbox", name="Select Origin City").click()
    page.get_by_text("BLR - BANGALORE INDIA IN").click()
    page.get_by_role("textbox", name="Select Destination City").click()
    page.get_by_text("DEL - DELHI INDIA IN").click()
    page.get_by_role("button", name="Search").click()

    # Wait for results
    page.wait_for_timeout( timeout=5000)

    # Extract details
    flights = page.locator(".flight-listing")
    count = flights.count()

    flight_results = []
    searchdatetime = datetime.now().isoformat()
    origin = "Bangalore"
    destination = "Delhi"

    for i in range(count):
        flight = flights.nth(i)
        name = flight.locator(".flight-name").inner_text()
        price = flight.locator(".flight-price").inner_text()
        duration = flight.locator(".flight-duration").inner_text()

        flight_results.append({
            "name": name,
            "price": price,
            "duration": duration,
            "searchdatetime": searchdatetime,
            "origin": origin,
            "destination": destination
        })

    # Save once — after adding all data
    with open("flight_results.json", "w") as f:
        json.dump(flight_results, f, indent=4)

    print(" flight_results.json saved successfully!")
    with open("flight_results.json", "r") as f:
        data = json.load(f)
        print(json.dumps(data, indent=4))

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
