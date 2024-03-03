# import libraries
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
import json
from dotenv import load_dotenv
import os


def setup_lt_options():
    '''
    Load and setup options for LambdaTest
    '''

    with open('./lt_options.json', 'r') as l:
        lt_options = json.load(l)

    # load username and access key from a `.env` file
    load_dotenv('./lambdaTest.env')
    lt_options["username"] = os.environ.get("USER")
    lt_options["accessKey"] = os.environ.get("ACCESS_KEY")

    return lt_options


def login_to_website(driver):
    '''
    Login to website for testing
    '''
    # select the relevant fields to log into the website
    username = driver.find_element("name", "user-name")
    password = driver.find_element("name", "password")
    submit_button = driver.find_element("name", "login-button")

    # enter the accepted username and password
    username.send_keys("standard_user")
    password.send_keys("secret_sauce")

    # Click the submit button
    submit_button.click()


class TestLoginPage(unittest.TestCase):
    def setUp(self):

        username = os.environ.get("USER")
        access_key = os.environ.get("ACCESS_KEY")

        # load lambdaTest configurations
        lt_options = setup_lt_options()

        # load browser configurations
        options = EdgeOptions()
        options.browser_version = "120.0"
        options.platform_name = "Windows 11"
        options.set_capability('LT:Options', lt_options)

        # Start the browser
        gridURL = "https://{}:{}@hub.lambdatest.com/wd/hub".format(
            username, access_key)
        self.driver = webdriver.Remote(
            command_executor=gridURL,
            options=options
        )
        # self.driver = webdriver.Remote(
        #     command_executor="http://hub.lambdatest.com:80/wd/hub",
        #     options=options)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

        # Go to the app home page
        self.driver.get("https://www.saucedemo.com/")

    def test_login(self):
        '''
        Test Login functionality of the page
        '''
        # select the relevant fields to log into the website
        username = self.driver.find_element("name", "user-name")
        password = self.driver.find_element("name", "password")
        submit_button = self.driver.find_element("name", "login-button")

        # enter the accepted username and password
        username.send_keys("standard_user")
        password.send_keys("secret_sauce")

        # Click the submit button
        submit_button.click()

        # Find products
        product_title = self.driver.find_element(By.CLASS_NAME, 'title')

        # check that the title is the same as displayed on the main page
        self.assertEqual(product_title.text, "Products",
                         "Main page title not found")

        # Indicate that the test has passed since the Assert is not raised
        self.driver.execute_script("lambda-status=passed")

    def test_logout(self):
        '''
        Test Logout Functionality of thr Application
        '''

        login_to_website(self.driver)

        # find hamburger menu button
        hamburger_button = self.driver.find_element(
            By.ID, "react-burger-menu-btn")
        # Click the submit button
        hamburger_button.click()

        # find logout button
        logout_button = self.driver.find_element(By.ID, "logout_sidebar_link")
        # Click the logout button
        logout_button.click()

        # Find login button
        login_btn = self.driver.find_element("name", "login-button")
        # assert if the Login button is displayed on the next page.
        self.assertTrue(login_btn.is_displayed(
        ), "Logout Unsuccessful, Login button not found on the final page")

        # Indicate that the test has passed since the Assert is not raised
        self.driver.execute_script("lambda-status=passed")

    def tearDown(self):
        self.driver.quit()


class TestPlatform(unittest.TestCase):

    def setUp(self):

        username = os.environ.get("USER")
        access_key = os.environ.get("ACCESS_KEY")

        # load lambdaTest configurations
        lt_options = setup_lt_options()

        # load browser configurations
        options = EdgeOptions()
        options.browser_version = "120.0"
        options.platform_name = "Windows 11"
        options.set_capability('LT:Options', lt_options)

        # Start the browser
        gridURL = "https://{}:{}@hub.lambdatest.com/wd/hub".format(
            username, access_key)
        self.driver = webdriver.Remote(
            command_executor=gridURL,
            options=options
        )
        # self.driver = webdriver.Remote(
        #     command_executor="http://hub.lambdatest.com:80/wd/hub",
        #     options=options)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        # Go to the app home page
        self.driver.get("https://www.saucedemo.com/")

        # Login to the website by default
        login_to_website(self.driver)

    def test_cart_badge_update(self):
        '''
        Add an item to cart and check if cart is updated
        '''

        # Locate the add to cart button and click it
        add_to_cart_button = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(
                ("name", 'add-to-cart-sauce-labs-backpack'))
        )
        add_to_cart_button.click()

        # Wait for the cart to update (you may need to adjust the time based on your website)
        WebDriverWait(self.driver, 3).until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "shopping_cart_badge"), '1')
        )
        badge_count = self.driver.find_element(
            By.CLASS_NAME, "shopping_cart_badge").text

        self.assertEqual(badge_count, '1', "Cart count not updated to 1")

        # Locate the add to cart button and click it
        add_to_cart_button = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(
                ("name", 'add-to-cart-sauce-labs-bike-light'))
        )
        add_to_cart_button.click()

        # Wait for the cart to update (you may need to adjust the time based on your website)
        WebDriverWait(self.driver, 3).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@class="shopping_cart_badge"]'), '2')
        )
        badge_count = self.driver.find_element(
            By.XPATH, '//*[@class="shopping_cart_badge"]').text

        self.assertEqual(badge_count, '2', "Cart count not updated to 2")

        # Indicate that the test has passed since the Assert is not raised
        self.driver.execute_script("lambda-status=passed")

    def test_add_to_cart_functionality(self):
        '''
        Add an item to cart and verify correct item is displayed in the cart
        '''
        # Locate the add to cart button and click it
        add_to_cart_button = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(
                ("name", 'add-to-cart-sauce-labs-backpack'))
        )
        # Click add to cart button
        add_to_cart_button.click()

        # Wait for the cart to update (you may need to adjust the time based on your website)
        WebDriverWait(self.driver, 3).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@class="shopping_cart_badge"]'), '1')
        )
        # Click on cart button
        cart_button = self.driver.find_element(
            By.CLASS_NAME, "shopping_cart_link")
        cart_button.click()

        item_name = self.driver.find_element(
            By.CLASS_NAME, "inventory_item_name").text

        self.assertEqual(item_name, "Sauce Labs Backpack",
                         "Added item not found in cart")

        # Indicate that the test has passed since the Assert is not raised
        self.driver.execute_script("lambda-status=passed")

    def test_continue_shopping(self):
        '''
        Test the following workflow.
        1. Add items to cart
        2. View Cart
        3. Click on `continue shopping` to view more items to add
        '''

        # Locate the add to cart button and click it
        add_to_cart_button = WebDriverWait(self.driver, 3).until(
            EC.element_to_be_clickable(
                ("name", 'add-to-cart-sauce-labs-backpack'))
        )
        # Click add to cart button
        add_to_cart_button.click()

        # Wait for the cart to update (you may need to adjust the time based on your website)
        WebDriverWait(self.driver, 3).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@class="shopping_cart_badge"]'), '1')
        )
        # Click on cart button
        cart_button = self.driver.find_element(
            By.CLASS_NAME, "shopping_cart_link")
        cart_button.click()

        # Click on continue shopping
        continue_shopping = self.driver.find_element(
            "name", 'continue-shopping')
        continue_shopping.click()

        # Find products
        product_title = self.driver.find_element(By.CLASS_NAME, 'title')

        # check that the title is the same as displayed on the main page
        self.assertEqual(product_title.text, "Products",
                         "Main page title not found")

        # Indicate that the test has passed since the Assert is not raised
        self.driver.execute_script("lambda-status=passed")

    def tearDown(self):
        self.driver.quit()
