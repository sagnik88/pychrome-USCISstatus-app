import time
import os
import boto3
import datetime
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from webdriver_wrapper import WebDriverWrapper
from selenium.webdriver.common.keys import Keys


def lambda_handler(*args, **kwargs):
    driver = WebDriverWrapper()
    receiptnumber = os.getenv("RECEIPTNUMBER")
    now = datetime.datetime.now()
    date_time = now.strftime("%Y%m%d")
    driver.get_url('https://egov.uscis.gov/casestatus/landing.do')
    driver.set_input_value('/html/body/div[2]/form/div/div[1]/div/div[1]/fieldset/div[1]/div[4]/input', receiptnumber)
    driver.click('/html/body/div[2]/form/div/div[1]/div/div[1]/fieldset/div[2]/div[2]/input')
    example_text = driver.get_inner_html('(//div//h1)[1]')
    client = boto3.resource('dynamodb')
    table = client.Table("receipt_status")
    driver.close()
    response = table.query(
        KeyConditionExpression=Key('receipt_number').eq(receiptnumber),
        ScanIndexForward=False
    )
    item = response['Items']
    receipt_status_old = item[0]["receipt_status"]
    last_updated = item[0]["update_date"]
    if example_text == receipt_status_old:
        status = "No change in status"
        send_email('sagnik88@gmail.com', 'sagnik88@gmail.com', receiptnumber, example_text)
    else:
        status = "Change in status"
        update_item(receiptnumber, date_time, example_text)
        send_email('sagnik88@gmail.com', 'sagnik88@gmail.com', receiptnumber, example_text)
        table.put_item(Item={'receipt_number': receiptnumber, 'update_date': date_time, 'receipt_status': example_text})
    return example_text


def update_item(receiptnumber, update_date, receiptstatus_val):
    try:
        dynamodb = boto3.resource('dynamodb', 'us-east-1')
        table = dynamodb.Table('receipt_status')
        set_update_date = str(update_date)
        response = table.update_item(
            Key={
                "receipt_number": receiptnumber,
                "update_date": str(update_date)
            },
            UpdateExpression="set receipt_status=:new_receipt_status",
            ExpressionAttributeValues={
                ":new_receipt_status": receiptstatus_val
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception as msg:
        print(f"Oops, could not update: {msg}")


def send_email(sender_email, recipient_email, receipt_no, receipt_stat):
    sender = "Sender Name <"+sender_email+">"
    recipient = recipient_email
    aws_region = "us-east-1"

    # The subject line for the email.
    subject = "Update to USCIS status for receipt number:" + receipt_no

    # The email body for recipients with non-HTML email clients.
    body_text = ("Update to USCIS status for receipt number:" + receipt_no + "\r\n" +
                 "The receipt status has been updated to " + receipt_stat
                 )

    # The HTML body of the email.
    body_html = """<html>
     <head></head>
     <body>
       <h1>Update to USCIS status for receipt number: """ + receipt_no + """</h1>
       <p>The receipt status has been updated to: """ + receipt_stat + """</p>
     </body>
     </html>
                 """

    # The character encoding for the email.
    charset = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=aws_region)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': charset,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': charset,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])