from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import os
from dotenv import load_dotenv

load_dotenv()


# for path use ABSOLUTE path to .exe file
DRIVER_PATH = "D:\\Development\\Internship\\automate-linkedin\\webdrivers\\chromedriver.exe"
driver = webdriver.Chrome(DRIVER_PATH)

main_url = "https://www.linkedin.com/"


# Main decorator
def main_func(func):
    """
    Decorator to login and execute other functions
    """
    def wrapper(*args, **kwargs):
        try:
            driver.get(url=main_url)

            # looking for field to ligin
            login_field = driver.find_element(By.ID, "session_key")
            password_field = driver.find_element(By.ID, "session_password")

            # inserting login and password
            login_field.send_keys(os.getenv("LOGIN"))
            password_field.send_keys(os.getenv("PASSWORD"))

            # Submitting
            submit = driver.find_element(
                By.XPATH, "//button[@type='submit']").click()

            # Outer function to be executed
            res = func(*args, **kwargs)
            time.sleep(1)
            return res

        except Exception as ex:
            print(ex)

        finally:
            time.sleep(2)
            driver.close()
            driver.quit()

    return wrapper


@main_func
def post_func(user_id):

    with open("post", "r") as f:
        message = f.read()

        driver.get(f"https://www.linkedin.com/in/{user_id}/overlay/create-post/")
        input_field = driver.find_element(By.TAG_NAME, "p")
        input_field.send_keys(message)
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        post_btn = [b for b in all_buttons if b.text == "Post"]
        post_btn[0].click()
    

if __name__ == "__main__":

    post_func(os.getenv("USER_ID"))
