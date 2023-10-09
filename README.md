# Halifax Mortgage Scraper

## Overview
This Python script, named `mortgage.py`, automates the process of retrieving mortgage rate information from a specific web page using Selenium, a tool for automating web browsers. The script also includes functionality to send notifications to a Slack channel using a webhook.

![screenshot](./images/bot.png)

## Dependencies
- `os`: For accessing environment variables.
- `time`: Used for pausing the script execution.
- `requests`: To send HTTP requests, specifically to send messages to Slack.
- `selenium`: A web browser automation tool.

## Environment Variables
- `SLACK_WEBHOOK_URL`: URL of the Slack webhook used for sending notifications to a Slack channel.
- `PURCHASE_PRICE`: The purchase price of the property.
- `DOWN_PAYMENT`: The down payment for the mortgage.

## Functions
### send_to_slack(message)
Sends a message to a Slack channel.
- `message`: The message text to be sent to Slack.

## Main Script Workflow
1. **Browser Initialization**: Sets up a headless Chrome browser for automation.
2. **Navigate and Interact with Web Page**:
    - Navigates to the Halifax mortgage calculator web page.
    - Automates various interactions like clicking buttons and filling out forms on the page.
3. **Sleep Delays**: Uses `time.sleep` to wait for certain elements to load or actions to complete.
4. **Find Mortgage Rates**:
    - Scrolls to the bottom of the page.
    - Finds elements containing mortgage rate information.
    - Specifically looks for a "5 Year Fixed Rate" mortgage with a product fee of £999.
5. **Send Notification to Slack**: If the desired mortgage rate is found, it sends a notification with the rate information to Slack using the `send_to_slack` function.
6. **Cleanup**: Closes the browser window to end the session.

## Notes
- The script is tightly coupled with the specific layout and elements of the Halifax mortgage calculator web page, meaning any changes to the web page could break the script.
- Delays and sleeps are hardcoded, which may not be optimal for different network speeds or web page response times.
- Error handling, particularly around web interactions and Slack notifications, is minimal and could be expanded for robustness.
- The script assumes that the environment variables are correctly set before execution.
