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
        options.add_argument("--headless=new")  # Enable headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        
        # Clear the ChromeDriver cache and download specific version
        import shutil
        import os
        
        # Clear the webdriver cache
        cache_path = os.path.join(os.path.expanduser("~"), ".wdm")
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)
        
        try:
            # Use undetected-chromedriver as a more reliable alternative
            self.driver = uc.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 20)
        except Exception as e:
            logging.error(f"Failed to create Chrome driver: {str(e)}")
            raise

    def login(self):
        """Login to Naukri.com"""
        try:
            logging.info("Attempting to login to Naukri.com")
            self.driver.get("https://www.naukri.com/nlogin/login")
            time.sleep(5)  # Wait for page to load completely
            
            # Updated selectors for login fields
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "usernameField"))
            )
            email_field.send_keys(self.email)
            
            # Fill password
            password_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "passwordField"))
            )
            password_field.send_keys(self.password)
            
            # Click login button
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(), 'Login')]"))
            )
            login_button.click()
            
            # Wait for login to complete
            time.sleep(5)  # Additional wait to ensure login completes
            logging.info("Successfully logged in to Naukri.com")
            return True

        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            return False

    def update_profile(self):
        """Update the profile to refresh timestamp"""
        try:
            # Navigate to profile section
            logging.info("Navigating to profile section")
            self.driver.get("https://www.naukri.com/mnjuser/profile")
            time.sleep(5)  # Wait for page to load completely

            # Find the resume headline section
            logging.info("Looking for resume headline section")
            resume_section = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'widgetHead')]//span[contains(text(), 'Resume headline')]"))
            )
            
            # Find and click the edit icon within the resume section
            logging.info("Clicking edit button")
            edit_icon = resume_section.find_element(By.XPATH, "..//span[contains(@class, 'edit icon')]")
            self.driver.execute_script("arguments[0].click();", edit_icon)
            time.sleep(3)  # Wait longer for the edit form to appear
            
            # Find and click the save button with the exact path
            logging.info("Looking for save button")
            save_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'form-actions')]//button[@type='submit' and contains(@class, 'btn-dark-ot')]"))
            )
            logging.info("Clicking save button")
            self.driver.execute_script("arguments[0].click();", save_button)
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
