import os
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import logging
import undetected_chromedriver as uc
import shutil

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('naukri_updater.log'),
        logging.StreamHandler()
    ]
)

class NaukriProfileUpdater:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv('NAUKRI_EMAIL')
        self.password = os.getenv('NAUKRI_PASSWORD')
        self.setup_driver()

    def setup_driver(self):
        """Set up Chrome driver with necessary options"""
        options = uc.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Add more realistic browser parameters
        options.add_argument("--enable-javascript")
        options.add_argument("--disable-notifications")
        options.add_argument('--disable-popup-blocking')
        options.add_argument("--ignore-certificate-errors")
        
        # Add user agent
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
        
        try:
            self.driver = uc.Chrome(options=options)
            
            # Additional stealth settings
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            
            self.wait = WebDriverWait(self.driver, 20)
            logging.info("Chrome driver setup complete")
        except Exception as e:
            logging.error(f"Failed to create Chrome driver: {str(e)}")
            raise

    def login(self):
        """Login to Naukri.com"""
        try:
            logging.info("Attempting to login to Naukri.com")
            self.driver.get("https://www.naukri.com/nlogin/login")
            
            # Add random delay to appear more human-like
            time.sleep(random.uniform(3, 5))

            # Wait for and enter email
            logging.info("Entering email")
            email_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder*="Enter Email ID / Username"]'))
            )
            email_field.clear()
            for char in self.email:
                email_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))

            time.sleep(random.uniform(1, 2))

            # Wait for and enter password
            logging.info("Entering password")
            password_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder*="Enter Password"]'))
            )
            password_field.clear()
            for char in self.password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))

            time.sleep(random.uniform(1, 2))

            # Click login button using multiple methods
            logging.info("Clicking login button")
            try:
                login_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
                )
                
                # Move mouse to button (even in headless mode)
                self.driver.execute_script("""
                    var event = new MouseEvent('mouseover', {
                        'view': window,
                        'bubbles': true,
                        'cancelable': true
                    });
                    arguments[0].dispatchEvent(event);
                """, login_button)
                
                time.sleep(random.uniform(0.5, 1))
                
                # Try regular click first
                try:
                    login_button.click()
                except:
                    # If regular click fails, try JavaScript click
                    self.driver.execute_script("arguments[0].click();", login_button)
            except Exception as e:
                logging.error(f"Failed to click login button: {str(e)}")
                return False

            # Wait for login to complete with random delay
            time.sleep(random.uniform(4, 6))
            
            # Verify login success
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="nI-gNb-drawer"]'))
                )
                logging.info("Successfully logged in to Naukri.com")
                
                # Navigate to profile section with random delay
                logging.info("Navigating to profile section")
                self.driver.get("https://www.naukri.com/mnjuser/profile")
                time.sleep(random.uniform(4, 6))
                return True
            except:
                logging.error("Login verification failed")
                return False

        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            return False

    def update_profile(self):
        """Update Naukri profile"""
        try:
            logging.info("Looking for resume headline section")
            # Wait for the page to load completely
            time.sleep(5)
            
            # Find edit button
            edit_button = self.driver.find_element(By.XPATH, '//*[@id="lazyResumeHead"]/div/div/div[1]/span[2]')
            if not edit_button:
                logging.error("Edit button not found")
                return False

            # Click edit button using JavaScript
            logging.info("Clicking edit button")
            self.driver.execute_script("arguments[0].click();", edit_button)

            # Wait for the save button to appear
            time.sleep(3)
            logging.info("Looking for save button")
            
            # Find save button
            save_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            if not save_button:
                logging.error("Save button not found")
                return False

            # Scroll to and click save button using JavaScript
            logging.info("Clicking save button")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", save_button)

            # Wait for the save to complete
            time.sleep(3)
            logging.info("Profile successfully updated")
            return True

        except Exception as e:
            logging.error(f"Profile update failed: {str(e)}")
            return False

    def close(self):
        """Close the browser"""
        self.driver.quit()

def main():
    ra = 0
    updater = None
    try:
        # Create updater instance and login only once
        logging.info("Starting Naukri Profile Updater")
        updater = NaukriProfileUpdater()
        
        if not updater.email or not updater.password:
            logging.error("Email or password not found in .env file")
            return

        # Login once at the start
        if not updater.login():
            logging.error("Initial login failed")
            return

        while True:
            try:
                if updater.update_profile():
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logging.info(f"Profile updated successfully at {current_time}")
                
                # Random interval between 2 to 12 minutes
                wait_time = random.randint(120, 720)
                logging.info(f"Waiting for {wait_time} seconds before next update")
                time.sleep(wait_time)

            except Exception as e:
                ra = ra + 1
                if ra == 3:
                    if updater:
                        updater.close()
                    exit()
                logging.error(f"An error occurred: {str(e)}")
                time.sleep(10)
                
                # If error occurs, try to login again
                try:
                    updater.login()
                except:
                    pass

    except KeyboardInterrupt:
        logging.info("Shutting down gracefully...")
        if updater:
            updater.close()

if __name__ == "__main__":
    main()
