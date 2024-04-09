from os import environ
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from dotenv import load_dotenv
import json
import os

def setup_lt_options():
    '''
    Load and setup options for LambdaTest
    '''
    with open('./lt_options.json', 'r') as l:
        lt_options = json.load(l)

    # load username and access key from a `.env` file
    load_dotenv('./lambdaTest.env')
    
    return lt_options

class PyUnitTestSetup:
    def __init__(self):
        # # Set LambdaTest options
        # lt_options = {
        #     'build': 'Build: Python Unittest Demo',
        #     'project': 'Project: Python Unittest Demo',
        #     'name': 'Test: Python Unittest Demo',
        #     'platform': 'Windows 11',
        #     'browserName': 'Chrome',
        #     'version': 'latest',
        #     'visual': False,  # Enable visual testing
        #     'network': True,  # Enable network capture
        #     'console': True,  # Enable console logs
        #     'video': True,  # Enable video recording
        # }

        '''
        Load and setup options for LambdaTest
        '''
        with open('./lt_options.json', 'r') as l:
            lt_options = json.load(l)

        # load username and access key from a `.env` file
        load_dotenv('./lambdaTest.env')

        # Get environment variables
        lt_username = environ.get('LT_USERNAME', None)
        lt_access_key = environ.get('LT_ACCESS_KEY', None)

        # Initialize Edge browser with LambdaTest options
        chrome_options = ChromeOptions()
        chrome_options.set_capability('LT:Options', lt_options)
        self.driver = webdriver.Remote(
            command_executor=f"https://{lt_username}:{lt_access_key}@hub.lambdatest.com/wd/hub",
            options=chrome_options
        )

        # self.driver = webdriver.Chrome()

    def setUp(self):
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def tearDown(self):
        if self.driver:
            self.driver.quit()