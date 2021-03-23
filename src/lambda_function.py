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
        status = "No change in status"
        print("No change in status")
    else:
        status="Change in status"
        print("Change in status")
        table.put_item(Item={'receipt_number': receiptnumber, 'update_date': date_time, 'receipt_status': example_text})
        # Replace sender@example.com with your "From" address.
        # This address must be verified with Amazon SES.
        SENDER = "Sender Name <sagnik88@gmail.com>"

        # Replace recipient@example.com with a "To" address. If your account
        # is still in the sandbox, this address must be verified.
        RECIPIENT = "sagnik88@gmail.com"

        # Specify a configuration set. If you do not want to use a configuration
        # set, comment the following variable, and the
        # ConfigurationSetName=CONFIGURATION_SET argument below.
        # CONFIGURATION_SET = "ConfigSet"

        # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
        AWS_REGION = "us-east-1"

        # The subject line for the email.
        SUBJECT = "Update to USCIS status for receipt number:" + receiptnumber

        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = ("Update to USCIS status for receipt number:" + receiptnumber + "\r\n" +
                     "The receipt status has been updated to " + status
                     )

        # The HTML body of the email.
        BODY_HTML = """<html>
        <head></head>
        <body>
          <h1>Update to USCIS status for receipt number: """ + receiptnumber + """</h1>
          <p>The receipt status has been updated to: """ + status + """</p>
        </body>
        </html>
                    """

        # The character encoding for the email.
        CHARSET = "UTF-8"

        # Create a new SES resource and specify a region.
        client = boto3.client('ses', region_name=AWS_REGION)

        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
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

    return example_text
