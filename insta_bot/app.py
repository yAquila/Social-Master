import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import streamlit as st
from webdriver_manager.chrome import ChromeDriverManager
from modules.utils import add_bg_from_local, set_page_config
from selenium.webdriver.support import expected_conditions as EC

DELAY_TIME = 2


class HomePage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.driver.get("https://www.instagram.com/")
        self.wait = wait

    def go_to_login_page(self):
        try:
            # time.sleep(DELAY_TIME)
            goto_login_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='Log in']"))
            )
            self.driver.execute_script("arguments[0].click();", goto_login_button)
            # self.driver.find_element.click()
        except:
            pass
        return LoginPage(self.driver, self.wait)


class LoginPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def login(self, username, password):
        # time.sleep(DELAY_TIME)
        username_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='username']")
            )
        )
        password_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='password']")
            )
        )
        username_input.clear()
        password_input.clear()
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))
        )
        self.driver.execute_script("arguments[0].click();", login_button)

    def close_popups(self):
        time.sleep(DELAY_TIME)
        try:
            not_now_button1 = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//button[text()="Not Now"]')
                )
            )
            not_now_button1.click()
            not_now_button2 = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, '//div[text()="Not Now"]'))
            )
            not_now_button2.click()
        except Exception as e:
            print(e)

    def go_to_profile_page(self, username):
        return ProfilePage(self.driver, self.wait, username)


class ProfilePage:
    def __init__(self, driver, wait, username):
        time.sleep(DELAY_TIME)
        self.driver = driver
        self.wait = wait
        self.username = username
        self.driver.get(f"https://www.instagram.com/{username}")

    def go_to_followers_window(self):
        time.sleep(DELAY_TIME)
        followers_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"a[href='/{self.username}/followers/']")
            )
        )
        self.driver.execute_script("arguments[0].click();", followers_button)

    def go_to_following_window(self):
        time.sleep(DELAY_TIME)
        """
        following_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"a[href='/{self.username}/following/']")
            )
        )
        self.driver.execute_script("arguments[0].click();", following_button)
        """
        following_button = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, f'a[href="/{self.user_name.lower()}/following/"]')
            )
        )
        self.driver.execute_script("arguments[0].click();", following_button)

        # not_now_button2 = self.wait.until(EC.visibility_of_element_located())
        # self.driver.get(f"https://www.instagram.com/{self.username}/followers/")
        # time.sleep(DELAY_TIME)
        # self.driver.get(f"https://www.instagram.com/{self.username}/following/")

    """
    def go_to_followings_window(self):
        time.sleep(DELAY_TIME)
        followings_button = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, f"a[href='/{self.username}/following/']")
            )
        )
        self.driver.execute_script("arguments[0].click();", followings_button)
        # self.driver.get(f"https://www.instagram.com/{self.username}/following/")
    """

    def follow_followers(self, max_count=100):
        # time.sleep(DELAY_TIME)
        followers_dialog = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='_aano']"))
        )

        visible_followers_list = self.wait.until(
            EC.visibility_of_any_elements_located((By.TAG_NAME, "li"))
        )
        visible_followers = len(visible_followers_list)
        for _ in range(max_count // visible_followers + 1):
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
                followers_dialog,
            )
            # time.sleep(1)
        print("Scroll down finished")
        follow_buttons = self.wait.until(
            EC.visibility_of_any_elements_located((By.XPATH, "//*[text()='Follow']"))
        )
        print(f"{len(follow_buttons)} profile will be followed")
        for follow_button in follow_buttons:
            self.driver.execute_script("arguments[0].click();", follow_button)
            # time.sleep(1)
        print(f"{len(follow_buttons)} profile were followed")


def get_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless")
    options.add_argument("--window-size=1080x1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.implicitly_wait(DELAY_TIME)
    return driver


if "login" not in st.session_state:
    st.session_state.login = False
if "login_button_clicked" not in st.session_state:
    st.session_state.login_button_clicked = False
if "driver" not in st.session_state:
    st.session_state.driver = None
if "home_page" not in st.session_state:
    st.session_state.home_page = None
if "login_page" not in st.session_state:
    st.session_state.login_page = None
if "profile_page" not in st.session_state:
    st.session_state.profile_page = None


def login_button_callback():
    st.session_state.login_button_clicked = True


def main():
    set_page_config()

    background_img_path = os.path.join("static", "background", "main-bg.png")
    sidebar_background_img_path = os.path.join("static", "background", "side-bg.png")
    page_markdown = add_bg_from_local(
        background_img_path=background_img_path,
        sidebar_background_img_path=sidebar_background_img_path,
    )
    st.markdown(page_markdown, unsafe_allow_html=True)

    st.markdown(
        """<h1 style='text-align: center; color: black; font-size: 60px;'> 🤖 INSTA BOT </h1>
        <br>""",
        unsafe_allow_html=True,
    )

    st.text_input("Please enter your username:", key="username")
    st.text_input("Please enter your password:", type="password", key="password")
    st.text_input(
        "Please enter the username whose followers you want to follow:",
        key="influencer_username",
    )
    global DELAY_TIME
    DELAY_TIME = st.number_input(
        "Please enter the delay amount before opening each page:",
        min_value=1,
        max_value=5,
        value=3,
    )

    _, _, col3, _, _ = st.columns(5)
    button = col3.button("Login Account", on_click=login_button_callback)
    _, col2, _, col4, _ = st.columns(5)
    placeholder = st.empty()
    if st.session_state.login_button_clicked:
        try:
            if not st.session_state.login:
                driver = get_driver()
                st.session_state.driver = driver
                wait = WebDriverWait(driver, DELAY_TIME)
                home_page = HomePage(driver, wait)
                st.session_state.home_page = home_page
                with placeholder.container():
                    st.success("Instagram home page opened")
                login_page = home_page.go_to_login_page()
                st.session_state.login_page = login_page
                login_page.login(st.session_state.username, st.session_state.password)
                login_page.close_popups()
                with placeholder.container():
                    st.success("Instagram login successful")
                st.session_state.login = True
            if col2.button("Follow"):
                login_page = st.session_state.login_page
                profile_page = login_page.go_to_profile_page(st.session_state.username)
                # profile_page.go_to_followers_window()
                profile_page.go_to_following_window()
                with placeholder.container():
                    st.success("Followers dialog opened")
                # profile_page.follow_followers(max_count=100)
                with placeholder.container():
                    st.success("100 followers followed")
            if col4.button("Unfollow"):
                login_page = st.session_state.login_page
                profile_page = login_page.go_to_profile_page(st.session_state.username)
                profile_page.go_to_following_window()
                with placeholder.container():
                    st.success("Followers dialog opened")
                # profile_page.follow_followers(max_count=100)
                with placeholder.container():
                    st.success("100 followings unfollowed")
        except Exception as e:
            with placeholder.container():
                st.error("An exception occured. Please try again.")
                st.error(e)
                st.session_state.driver.get_screenshot_as_file("exception.png")


if __name__ == "__main__":
    main()
