# import libraries
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


'''XPATHS and Full XPATH Variables'''

#Test:1 - test_login Xpaths
Login_XPATH = """//*[@id="widget-navbar-217834"]/ul/li[6]/a"""
Login_Submit_XPATH ="""//*[@id="content"]/div/div[2]/div/div/form/input[1]"""
Login_Success_XPATH = """//*[@id="content"]/div[1]/h2"""

#Test:2 - test_logout Xpaths
Logout_XPATH = """//*[@id="column-right"]/div/a[14]"""
Logout_Success_XPATH = """//*[@id="content"]/h1"""

#Test:3 - test_cart_badge_update XPaths
Nav_to_Home_XPATH = """//*[@id="widget-navbar-217834"]/ul/li[1]/a"""
Buttons_XPATH = """/html/body/div[1]/div[5]/div[1]/div[7]/div/div[2]/div/div[2]/div/div[1]/div/div/div[1]"""
Quick_View_XPATH = """/html/body/div[1]/div[5]/div[1]/div[7]/div/div[2]/div/div[2]/div/div[1]/div/div/div[1]/div/div[1]/div[2]"""
Add_to_Cart_XPATH = Quick_View_XPATH+"/button[1]"
Cart_badge_XPATH =  """/html/body/div[1]/div[5]/header/div[2]/div[1]/div[5]/a/div[1]/span"""

#Test:4 - test_add_to_cart_functionality XPaths
#Also uses previous tests xpaths
Close_Notification_XPATH = """/html/body/div[2]/div/div[1]/button/span"""
Cart_Button_XPATH = """/html/body/div[1]/div[5]/header/div[2]/div[1]/div[5]/a/div[1]/div"""
Cart_Element_Item_XPATH = """/html/body/div[1]/div[3]/div/div[1]/div/table/tbody/tr/td[2]/a"""

#Test:5 - test_continue_shopping XPaths
Edit_Cart_XPATH = """/html/body/div[1]/div[3]/div/div[2]/div/div[1]/a"""
Continue_Shopping_XPATH = """/html/body/div[1]/div[5]/div[1]/div/div/div[2]/a[1]"""
Home_Title_XPATH = """/html/body/div[1]/div[5]/div[1]/div[3]/div/div[1]/h3"""

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

    login_button = driver.find_element(By.XPATH, Login_XPATH) # Go to login page
    
    login_button.click()

    # select the relevant fields to log into the website
    username = driver.find_element("name","email")
    password = driver.find_element("name","password")

    submit_button = driver.find_element(By.XPATH, Login_Submit_XPATH)

    # enter the accepted username and password
    username.send_keys("haziqa5122@gmail.com")
    password.send_keys("testuser")

    # Click the submit button
    submit_button.click()


class TestLoginPage(unittest.TestCase):
    def setUp(self):

	# load lambdaTest configurations
        lt_options = setup_lt_options()
        
        username = os.environ.get("LT_USERNAME")
        access_key = os.environ.get("LT_ACCESS_KEY")

        # load browser configurations
        options = ChromeOptions()
        options.platform_name = "Windows 11"
        options.set_capability('LT:Options', lt_options)

        # Start the browser
        gridURL = "https://{}:{}@hub.lambdatest.com/wd/hub".format(
            username, access_key)
            
        self.driver = webdriver.Remote(
            command_executor=gridURL,
            options=options
        )
        
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

        # Go to the app home page
        self.driver.get("https://ecommerce-playground.lambdatest.io/")

    def test_login(self):
        '''
        Test Login functionality of the page
        '''
        login_button = self.driver.find_element(By.XPATH, Login_XPATH) # Go to login page
        
        login_button.click()

        # select the relevant fields to log into the website
        username = self.driver.find_element("name","email")
        password = self.driver.find_element("name","password")
    
        submit_button = self.driver.find_element(By.XPATH, Login_Submit_XPATH)

        # enter the accepted username and password
        username.send_keys("haziqa5122@gmail.com")
        password.send_keys("testuser")

        # Click the submit button
        submit_button.click()

        # Login success response
        success_text = self.driver.find_element(By.XPATH, Login_Success_XPATH)

        # check that the title is the same as displayed on the main page
        self.assertEqual(success_text.text, "My Account",
                         "Credentials are Invalid")
        # Indicate that the test has passed since the Assert is not raised
        self.driver.execute_script("lambda-status=passed")

    def test_logout(self):
        '''
        Test Logout Functionality of thr Application
        '''

        login_to_website(self.driver)

        #Find logout button in the right panel of menu
        logout_button = self.driver.find_element(
            By.XPATH, Logout_XPATH)
        
        # Click the submit button
        logout_button.click()

        # Logout success response
        logout_text = self.driver.find_element(By.XPATH, Logout_Success_XPATH)
        # assert if the Login button is displayed on the next page.
        self.assertEqual(logout_text.text, "Account Logout","Logout unsuccessful, No response provided from the site.")

        # Indicate that the test has passed since the Assert is not raised
        self.driver.execute_script("lambda-status=passed")

    def tearDown(self):
        self.driver.quit()


class TestPlatform(unittest.TestCase):

    def setUp(self):

        # load lambdaTest configurations
        # load lambdaTest configurations
        lt_options = setup_lt_options()
        
        username = os.environ.get("LT_USERNAME")
        access_key = os.environ.get("LT_ACCESS_KEY")

        # load browser configurations
        options = ChromeOptions()
        options.platform_name = "Windows 11"
        options.set_capability('LT:Options', lt_options)

        # Start the browser
        gridURL = "https://{}:{}@hub.lambdatest.com/wd/hub".format(
            username, access_key)
            
        self.driver = webdriver.Remote(
            command_executor=gridURL,
            options=options
        )
        
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

        # Go to the app home page
        self.driver.get("https://ecommerce-playground.lambdatest.io/")

        # Login to the website by default
        login_to_website(self.driver)

    def test_cart_badge_update(self):
        '''
        Add an item to cart and check if cart is updated
        '''

        #Going to Home page
        home_button = self.driver.find_element(By.XPATH, Nav_to_Home_XPATH)
        home_button.click()

       
        #On hover, It provides option to add to cart
        hover_item1 = self.driver.find_element(By.XPATH, Buttons_XPATH)
    
        # Quick view the item and add to cart

        ActionChains(self.driver).move_to_element(hover_item1).perform()
        
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_all_elements_located((By.XPATH, Quick_View_XPATH ))
        )

        add_to_cart = self.driver.find_element(By.XPATH, Add_to_Cart_XPATH)

        # Wait for the cart to update (you may need to adjust the time based on your website)
        add_to_cart.click()

        WebDriverWait(self.driver, 3).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, Cart_badge_XPATH), '1'))

        badge_count = self.driver.find_element(By.XPATH, Cart_badge_XPATH)

        self.assertEqual(badge_count.text, '1', "Cart count not updated to 1")

        # Indicate that the test has passed since the Assert is not raised
        self.driver.execute_script("lambda-status=passed")

    def test_add_to_cart_functionality(self):
        '''
        Add an item to cart and verify correct item is displayed in the cart
        '''

        #Going to Home page
        home_button = self.driver.find_element(By.XPATH, Nav_to_Home_XPATH)
        home_button.click()

       
        #On hover, It provides option to add to cart
        hover_item1 = self.driver.find_element(By.XPATH, Buttons_XPATH)
    
        # Quick view the item and add to cart

        ActionChains(self.driver).move_to_element(hover_item1).perform()
        
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_all_elements_located((By.XPATH, Quick_View_XPATH ))
        )

        add_to_cart = self.driver.find_element(By.XPATH, Add_to_Cart_XPATH)

        # Wait for the cart to update (you may need to adjust the time based on your website)
        add_to_cart.click()

        #Close the notification
        self.driver.find_element(By.XPATH, Close_Notification_XPATH).click()

        #Click the shopping cart button
        self.driver.find_element(By.XPATH, Cart_Button_XPATH).click()

        WebDriverWait(self.driver, 3).until(
     EC.text_to_be_present_in_element(
            (By.XPATH, Cart_Element_Item_XPATH ), 'HTC Touch HD')
        )

        #Extract the item name from the cart
        item_name = self.driver.find_element(By.XPATH, Cart_Element_Item_XPATH).text

        self.assertEqual(item_name, "HTC Touch HD",
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

        #Going to Home page
        home_button = self.driver.find_element(By.XPATH, Nav_to_Home_XPATH)
        home_button.click()

       
        #On hover, It provides option to add to cart
        hover_item1 = self.driver.find_element(By.XPATH, Buttons_XPATH)
    
        # Quick view the item and add to cart

        ActionChains(self.driver).move_to_element(hover_item1).perform()
        
        WebDriverWait(self.driver, 3).until(
            EC.visibility_of_all_elements_located((By.XPATH, Quick_View_XPATH ))
        )

        add_to_cart = self.driver.find_element(By.XPATH, Add_to_Cart_XPATH)

        # Wait for the cart to update (you may need to adjust the time based on your website)
        add_to_cart.click()


        #Close the notification
        self.driver.find_element(By.XPATH, Close_Notification_XPATH).click()

        #Click the shopping cart button
        self.driver.find_element(By.XPATH, Cart_Button_XPATH).click()
        
        #Go to Edit cart option
        self.driver.find_element(By.XPATH, Edit_Cart_XPATH).click()
        
        #Go to continue shopping option
        self.driver.find_element(By.XPATH, Continue_Shopping_XPATH).click()

        #Extract the text from the main page
        product_title = self.driver.find_element(By.XPATH, Home_Title_XPATH)

        # check that the title is the same as displayed on the main page
        self.assertEqual(product_title.text, "TOP TRENDING CATEGORIES",
                         "Main page title not found")

        # Indicate that the test has passed since the Assert is not raised
        self.driver.execute_script("lambda-status=passed")

    def tearDown(self):
        self.driver.quit()
