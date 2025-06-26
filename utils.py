import random
import tempfile
import undetected_chromedriver as uc


HEADLESS = False


def setup_driver():
    """
    Initializes a Chrome WebDriver instance with undetected-chromedriver.
    """
    chrome_options = uc.ChromeOptions()

    # Use a unique temporary directory for each worker to avoid conflicts
    temp_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    chrome_options.add_argument(f"--data-path={temp_dir}")

    # General browser settings
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--disable-site-isolation-trials")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options = uc.ChromeOptions()

    # Disable popup blocking to allow new tabs

    # Headless Mode (Avoid Detection)
    chrome_options.headless = HEADLESS

    # Prevent detection by removing automation flags and using a random User-Agent
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Hide automation detection

    # Vietnamese user agents
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Pixel 3 XL Build/QQ1A.200205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.120 Mobile Safari/537.36",
    ]
    chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

    # Set the Accept-Language header to Vietnamese
    chrome_options.add_argument("--lang=vi-VN")


    try:
        driver = uc.Chrome(
            options=chrome_options,
            use_subprocess=True,
        )
        driver.maximize_window()  # Ensures window is maximized, even in headless mode
        return driver
    except Exception as e:
        raise Exception(f"Failed to initialize WebDriver: {e}")
