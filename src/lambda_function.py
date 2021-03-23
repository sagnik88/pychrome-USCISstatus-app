import time
import os
import boto3
import datetime
from boto3.dynamodb.conditions import Key

from webdriver_wrapper import WebDriverWrapper
from selenium.webdriver.common.keys import Keys


def lambda_handler(*args, **kwargs):
    driver = WebDriverWrapper()
    receiptnumber = os.getenv("RECEIPTNUMBER")
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    driver.get_url('https://egov.uscis.gov/casestatus/landing.do')
    driver.set_input_value('/html/body/div[2]/form/div/div[1]/div/div[1]/fieldset/div[1]/div[4]/input',receiptnumber)
    driver.click('/html/body/div[2]/form/div/div[1]/div/div[1]/fieldset/div[2]/div[2]/input')
    example_text = driver.get_inner_html('(//div//h1)[1]')
    print(example_text)
    client = boto3.resource('dynamodb')
    table = client.Table("receipt_status")
    print(table.table_status)
    # table.put_item(Item={'receipt_number': receiptnumber, 'update_date': date_time, 'receipt_status': example_text})
    driver.close()
    response = table.query(
        KeyConditionExpression=Key('receipt_number').eq(receiptnumber)
    )
    item = response['Items']
    receipt_status_old = item[0]["receipt_status"]
    print(receipt_status_old)
    if example_text == receipt_status_old:
        print("No change in status")
    else:
        print("Change in status")
        table.put_item(Item={'receipt_number': receiptnumber, 'update_date': date_time, 'receipt_status': example_text})

    return example_text
