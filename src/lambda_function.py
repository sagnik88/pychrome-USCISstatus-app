import time
import os

from webdriver_wrapper import WebDriverWrapper
from selenium.webdriver.common.keys import Keys


def lambda_handler(*args, **kwargs):
    driver = WebDriverWrapper()
    receiptnumber=os.getenv("RECEIPTNUMBER")
    driver.get_url('https://egov.uscis.gov/casestatus/landing.do')
    driver.set_input_value('/html/body/div[2]/form/div/div[1]/div/div[1]/fieldset/div[1]/div[4]/input',receiptnumber)
    driver.click('/html/body/div[2]/form/div/div[1]/div/div[1]/fieldset/div[2]/div[2]/input')
    example_text = driver.get_inner_html('(//div//h1)[1]')


    driver.close()

    return example_text
