import os
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # For automatic ChromeDriver installation
import logging
import urllib3
from ..abstract_webtools import *  # Assuming this is a valid import
from .urlManager import *

# Suppress urllib3 warnings and debug logs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("selenium").setLevel(logging.WARNING)

# Default Chrome options (can be overridden)
DEFAULT_CHROME_OPTIONS = [
    "--headless",  # Run in headless mode
    "--no-sandbox",
    "--disable-dev-shm-usage",  # Avoid memory issues on servers
    "--disable-gpu",
    "--disable-software-rasterizer",
    "--disable-extensions",
    "--remote-debugging-port=9222"
]

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class SeleniumManager(metaclass=SingletonMeta):
    def __init__(self, url):
        if not hasattr(self, 'initialized'):  # Prevent reinitialization
            self.initialized = True
            parsed_url = urlparse(url)
            self.domain = parsed_url.netloc
            self.scheme = parsed_url.scheme or "https"  # Default to https if scheme is missing
            self.base_url = f"{self.scheme}://{self.domain}"
            self.site_dir = os.path.join(os.getcwd(), self.domain)
            os.makedirs(self.site_dir, exist_ok=True)
            self.drivers = {}
            self.page_type = []

    def get_url_to_path(self, url):
        url = eatAll(str(url), ['', ' ', '\n', '\t', '\\', '/'])  # Assuming eatAll is defined elsewhere
        parsed_url = urlparse(url)
        if parsed_url.netloc == self.domain:
            paths = parsed_url.path.split('/')
            dir_path = self.site_dir
            for path in paths[:-1]:
                dir_path = os.path.join(dir_path, path)
                os.makedirs(dir_path, exist_ok=True)
            self.page_type.append(os.path.splitext(paths[-1])[-1] or 'html' if not self.page_type else self.page_type[-1])
            dir_path = os.path.join(dir_path, paths[-1])
            return dir_path

    def saved_url_check(self, url):
        return self.get_url_to_path(url)

    def get_with_netloc(self, url):
        parsed_url = urlparse(url)
        if not parsed_url.netloc:
            url = f"{self.scheme}://{self.domain}/{url.strip('/')}"
        return url

    def get_driver(self, url):
        if url and url not in self.drivers:
            # Set up Chrome options
            chrome_options = Options()
            for option in DEFAULT_CHROME_OPTIONS:
                chrome_options.add_argument(option)
            
            # Specify Chrome binary location if needed (optional, comment out if not applicable)
            # chrome_options.binary_location = "/home/profiles/solcatcher/.cache/selenium/chrome/linux64/130.0.6723.58/chrome"

            # Automatically install and use ChromeDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            self.drivers[url] = driver
            driver.get(url)
        return self.drivers[url]

    def quit_driver(self, url):
        """Clean up a specific driver instance."""
        if url in self.drivers:
            self.drivers[url].quit()
            del self.drivers[url]

    def quit_all_drivers(self):
        """Clean up all driver instances."""
        for driver in self.drivers.values():
            driver.quit()
        self.drivers.clear()

def normalize_url(url, base_url=None):
    """Normalize and resolve relative URLs."""
    manager = SeleniumManager(url)
    base_url = manager.base_url if base_url is None else base_url
    if url.startswith(base_url):
        url = url[len(base_url):]
    normalized_url = urljoin(base_url, url.split('#')[0])
    if not normalized_url.startswith(base_url):
        return None
    return normalized_url

def get_selenium_source(url):
    """Fetch page source using Selenium."""
    url_mgr = urlManager(url)  # Assuming urlManager is defined elsewhere
    if url_mgr.url:
        url = str(url_mgr.url)
        manager = SeleniumManager(url)
        driver = manager.get_driver(url)
        try:
            return driver.page_source
        except Exception as e:
            logging.error(f"Error fetching page source for {url}: {e}")
            return None
        # Note: Driver is not quit here to maintain Singleton behavior

# Ensure cleanup on program exit (optional)
import atexit
atexit.register(lambda: SeleniumManager(url="").quit_all_drivers())  # Cleanup all drivers on exit
