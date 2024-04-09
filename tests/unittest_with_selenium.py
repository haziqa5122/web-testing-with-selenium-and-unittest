# import libraries
import sys

sys.path.append(sys.path[0] + "/..")

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.options import Options as ChromeOptions
import json
from dotenv import load_dotenv
import os
from pyunitsetup import PyUnitTestSetup

'''XPATHS and Full XPATH Variables'''

#Test:1 - test_login selectors
Login_Selector = """#widget-navbar-217834 > ul > li:nth-child(6) > a > div > span"""
# Login_Submit_XPATH ="""//*[@id="content"]/div/div[2]/div/div/form/input[1]"""
Login_Submit_locator = "[value='Login']"
Login_Success_Selector = """#content > div:nth-child(1) > h2"""
#Test:2 - test_logout selectors
Logout_Selector = """#column-right > div > a:nth-child(14)"""
Logout_Success_Selector = """#content > h1"""

#Test:3 - test_cart_badge_update Selectors
Nav_to_Home_Selector = """#widget-navbar-217834 > ul > li:nth-child(1) > a > div"""
Buttons_XPATH = """/html/body/div[1]/div[5]/div[1]/div[7]/div/div[2]/div/div[2]/div/div[1]/div/div/div[1]"""
Quick_View_XPATH = """/html/body/div[1]/div[5]/div[1]/div[7]/div/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div[1]/div[2]"""
Add_to_Cart_XPATH = Quick_View_XPATH+"/button[1]"
# Cart_badge_XPATH =  """/html/body/div[1]/div[5]/header/div[2]/div[1]/div[5]/a/div[1]/span"""
Cart_badge_locator = "span.badge.badge-pill.badge-info.cart-item-total"

#Test:4 - test_add_to_cart_functionality XPaths
#Also uses previous tests xpaths
Close_Notification_Selector = """#notification-box-top > div > div.toast-header > button > span"""
Cart_Button_Selector = """#entry_217825 > a > div.cart-icon > div > svg"""
Cart_Element_Item_Selector = """#entry_217847 > div > table > tbody > tr > td:nth-child(2) > a"""

#Test:5 - test_continue_shopping XPaths
Edit_Cart_XPATH = """#entry_217850 > a"""
Continue_Shopping_XPATH = """#content > div.buttons.d-flex > a.btn.btn-lg.btn-secondary.mr-auto"""
Home_Title_XPATH = """#entry_213249 > h3.module-title"""

# Initialize the PyUnitTestSetup fixture
# setup = PyUnitTestSetup()
# setup.setUp()  # Added setUp() method call here
# # driver = setup.driver

def setup_lt_options():
    '''
    Load and setup options for LambdaTest
    '''
    with open('./lt_options.json', 'r') as l:
        lt_options = json.load(l)

    # load username and access key from a `.env` file
    load_dotenv('./lambdaTest.env')
    
    return lt_options


def login_to_website(driver):
    '''
    Login to website for testing
    '''

    driver.get("https://ecommerce-playground.lambdatest.io/")

    login_button = driver.find_element(By.CSS_SELECTOR, Login_Selector) # Go to login page
    login_button.click()

    # select the relevant fields to log into the website
    username = driver.find_element("name","email")
    password = driver.find_element("name","password")

    submit_button = driver.find_element(By.CSS_SELECTOR, Login_Submit_locator)

    # enter the accepted username and password
    username.send_keys("haziqa5122@gmail.com")
    password.send_keys("testuser")

    # Click the submit button
    submit_button.click()

class TestLoginPage(unittest.TestCase):

    def test_login(self):
        '''
        Test Login functionality of the page
        '''

        setup = PyUnitTestSetup()
        setup.setUp()  # Added setUp() method call here
        driver = setup.driver

        driver.get("https://ecommerce-playground.lambdatest.io/")

        login_button = driver.find_element(By.CSS_SELECTOR, Login_Selector) # Go to login page
        
        login_button.click()

        # select the relevant fields to log into the website
        username = driver.find_element("name","email")
        password = driver.find_element("name","password")
    
        submit_button = driver.find_element(By.CSS_SELECTOR, Login_Submit_locator)

        # enter the accepted username and password
        username.send_keys("haziqa5122@gmail.com")
        password.send_keys("testuser")

        # Click the submit button
        submit_button.click()

        # Login success response
        success_text = driver.find_element(By.CSS_SELECTOR, Login_Success_Selector)

        # check that the title is the same as displayed on the main page
        self.assertEqual(success_text.text, "My Account",
                         "Credentials are Invalid")
    #     # Indicate that the test has passed since the Assert is not raised
        driver.execute_script("lambda-status=passed")
        
        setup.tearDown()

    def test_logout(self):
        '''
        Test Logout Functionality of thr Application
        '''

        setup = PyUnitTestSetup()
        setup.setUp()  # Added setUp() method call here
        driver = setup.driver

        login_to_website(driver)

        #Find logout button in the right panel of menu
        logout_button = driver.find_element(
            By.CSS_SELECTOR, Logout_Selector)
        
        # Click the submit button
        logout_button.click()

        # Logout success response
        logout_text = driver.find_element(By.CSS_SELECTOR, Logout_Success_Selector)
        # assert if the Login button is displayed on the next page.
        self.assertEqual(logout_text.text, "Account Logout","Logout unsuccessful, No response provided from the site.")

        # Indicate that the test has passed since the Assert is not raised
        setup.driver.execute_script("lambda-status=passed")

        setup.tearDown()


class TestPlatform(unittest.TestCase):

    def test_cart_badge_update(self):
        '''
        Add an item to cart and check if cart is updated
        '''

        setup = PyUnitTestSetup()
        setup.setUp()  # Added setUp() method call here
        driver = setup.driver

        driver.get("https://ecommerce-playground.lambdatest.io/")

        #Going to Home page
        home_button = driver.find_element(By.CSS_SELECTOR, Nav_to_Home_Selector)
        home_button.click()

        #On hover, It provides option to add to cart
        hover_item1 = driver.find_element(By.XPATH, Buttons_XPATH)
    
        # Quick view the item and add to cart

        ActionChains(driver).move_to_element(hover_item1).perform()
        
        WebDriverWait(driver, 3).until(
            EC.visibility_of_all_elements_located((By.XPATH, Quick_View_XPATH))
        )

        add_to_cart = driver.find_element(By.XPATH, Add_to_Cart_XPATH)

        add_to_cart.click()


        badge_count = driver.find_elements(By.CLASS_NAME, Cart_badge_locator)
        # Check if any elements were found
        if badge_count:
            # Access the first element (index 0)
            badge_count_elem = badge_count[0]
            self.assertNotEqual(badge_count_elem.text, '0', "Cart count not updated")

        # Indicate that the test has passed since the Assert is not raised
        driver.execute_script("lambda-status=passed")

        setup.tearDown()

    def test_add_to_cart_functionality(self):
        '''
        Add an item to cart and verify correct item is displayed in the cart
        '''

        setup = PyUnitTestSetup()
        setup.setUp()  # Added setUp() method call here
        driver = setup.driver

        driver.get("https://ecommerce-playground.lambdatest.io/")

        #Going to Home page
        home_button = driver.find_element(By.CSS_SELECTOR, Nav_to_Home_Selector)
        home_button.click()

       
        #On hover, It provides option to add to cart
        hover_item1 = driver.find_element(By.XPATH, Buttons_XPATH)
    
        # Quick view the item and add to cart

        ActionChains(driver).move_to_element(hover_item1).perform()
        
        WebDriverWait(driver, 3).until(
            EC.visibility_of_all_elements_located((By.XPATH, Quick_View_XPATH ))
        )

        add_to_cart = driver.find_element(By.XPATH, Add_to_Cart_XPATH)

        # Wait for the cart to update (you may need to adjust the time based on your website)
        add_to_cart.click()

        #Close the notification
        driver.find_element(By.CSS_SELECTOR, Close_Notification_Selector).click()

        #Click the shopping cart button
        driver.find_element(By.CSS_SELECTOR, Cart_Button_Selector).click()

        WebDriverWait(driver, 3).until(
     EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, Cart_Element_Item_Selector ), 'HTC Touch HD')
        )

        #Extract the item name from the cart
        item_name = driver.find_element(By.CSS_SELECTOR, Cart_Element_Item_Selector).text

        self.assertEqual(item_name, "HTC Touch HD",
                         "Added item not found in cart")

        # Indicate that the test has passed since the Assert is not raised
        driver.execute_script("lambda-status=passed")

        setup.tearDown()

    def test_continue_shopping(self):
        '''
        Test the following workflow.
        1. Add items to cart
        2. View Cart
        3. Click on `continue shopping` to view more items to add
        '''

        setup = PyUnitTestSetup()
        setup.setUp()  # Added setUp() method call here
        driver = setup.driver

        driver.get("https://ecommerce-playground.lambdatest.io/")

        #Going to Home page
        home_button = driver.find_element(By.CSS_SELECTOR, Nav_to_Home_Selector)
        home_button.click()

       
        #On hover, It provides option to add to cart
        hover_item1 = driver.find_element(By.XPATH, Buttons_XPATH)
    
        # Quick view the item and add to cart

        ActionChains(driver).move_to_element(hover_item1).perform()
        
        WebDriverWait(driver, 3).until(
            EC.visibility_of_all_elements_located((By.XPATH, Quick_View_XPATH))
        )

        add_to_cart = driver.find_element(By.XPATH, Add_to_Cart_XPATH)

        # Wait for the cart to update (you may need to adjust the time based on your website)
        add_to_cart.click()


        #Close the notification
        driver.find_element(By.CSS_SELECTOR, Close_Notification_Selector).click()

        #Click the shopping cart button
        driver.find_element(By.CSS_SELECTOR, Cart_Button_Selector).click()
        
        #Go to Edit cart option
        driver.find_element(By.CSS_SELECTOR, Edit_Cart_XPATH).click()
        
        #Go to continue shopping option
        driver.find_element(By.CSS_SELECTOR, Continue_Shopping_XPATH).click()

        #Extract the text from the main page
        product_title = driver.find_element(By.CSS_SELECTOR, Home_Title_XPATH)

        # check that the title is the same as displayed on the main page
        self.assertEqual(product_title.text, "TOP TRENDING CATEGORIES",
                         "Main page title not found")

        # Indicate that the test has passed since the Assert is not raised
        driver.execute_script("lambda-status=passed")

        setup.tearDown()

