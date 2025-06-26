from selenium import webdriver

# Initialize the WebDriver (e.g., Chrome)
driver = webdriver.Chrome()

# Open the first tab and go to a URL
driver.get("https://www.google.com")

# Get the list of all window handles
window_handles = driver.window_handles

# Open a second tab using JavaScript
driver.execute_script("window.open('');")
driver.switch_to.window(window_handles[-1])
driver.get("https://app.zoom.us/wc/join")

window_handles = driver.window_handles

driver.execute_script("window.open('');")
driver.switch_to.window(window_handles[-1])
driver.get("https://app.zoom.us/wc/join")

while True:
    q = input("Enter q to stop: ")
    if q == 'q':
        break
# Close the driver after finishing interactions
driver.quit()
