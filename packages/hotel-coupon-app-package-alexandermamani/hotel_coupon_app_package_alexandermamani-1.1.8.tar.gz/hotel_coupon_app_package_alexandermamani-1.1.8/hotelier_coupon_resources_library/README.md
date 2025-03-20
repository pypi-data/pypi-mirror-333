# hotel_coupon_app_package_alexandermamani

Custom libraries for the hotelier coupon app. This package includes the following classes:

- `ReportPDF`: Helps to generate a custom report PDF.
- `SNSService`: Manages interactions with AWS SNS.
- `SQSService`: Manages interactions with AWS SQS.

This package also includes the following Exceptions:

- `SNSPublishMessageError`: Exception raised for publishing SNS message error.
- `SQSPollingMessagesError`: Exception raised for polling SQS messages error.
- `SQSClosingConnectionError`: Exception raised for closing SQS connection error.

## Installation

To install the hotel coupon package, use:

```sh
pip install hotel-coupon-app-package-alexandermamani
```

## Usage

#### ReportPDF

```python
from hotel_coupon_app_package_alexandermamani.report_pdf import ReportPDF

coupon_gral_information = {}
coupon_gral_information['1'] = {}
coupon_gral_information['1']['title'] = "December offer"
coupon_gral_information['1']['how_many_have_redeemed'] = "2"
coupon_gral_information['1']['how_many_have_used'] = "1"
coupon_gral_information['1']['quantity'] = "30"
coupon_gral_information['1']['discount'] = "10"
coupon_gral_information['2'] = {}
coupon_gral_information['2']['title'] = "January offer"
coupon_gral_information['2']['how_many_have_redeemed'] = "0"
coupon_gral_information['2']['how_many_have_used'] = "0"
coupon_gral_information['2']['quantity'] = "15"
coupon_gral_information['2']['discount'] = "5"

user_interactions = {}
user_interactions["1"] = {}
user_interactions["1"]['view'] = 0
user_interactions["1"]['redeem'] = 0
user_interactions["1"]['coupon_title'] = "Winter promotion"
user_interactions["2"] = {}
user_interactions["2"]['view'] = 10
user_interactions["2"]['redeem'] = 10
user_interactions["2"]['coupon_title'] = "Summer promotion"

hotelier_name="Dublin hotel"
from_date_report=datetime.datetime.now().date()
report = ReportPDF(coupon_interaction_data=user_interactions,
                   coupon_gral_information_data=coupon_gral_information, 
                   from_date_report=from_date_report, 
                   hotelier_name=hotelier_name)

report_pdf_buffer = report.generate()
```


#### SNSService
To notify a specific user about a coupon usage, you can use the following code:
```python
from hotel_coupon_app_package_alexandermamani.aws_services import SNSService, SNSPublishMessageError
import environ

env = environ.Env()
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_REGION = env('AWS_REGION')
AWS_SNS_USED_COUPON_NOTIFICATION_ARN = env('AWS_SNS_USED_COUPON_NOTIFICATION_ARN')

message = { "user_profile_id": "u1s6574-234-123244342",
                "coupon_code": "uihj123123-123123-123"}

sns_service = SNSService(aws_access_key=AWS_ACCESS_KEY_ID, 
                         aws_secret_key=AWS_SECRET_ACCESS_KEY, 
                         region_name=AWS_REGION)
try:
    sns_service.publish_message(target_arn=AWS_SNS_USED_COUPON_NOTIFICATION_ARN, 
                                message=message, 
                                subject="Report Notification")
except SNSPublishMessageError as e:
    print("SNS Error", e)

```


#### SQSService

#### Example of polling user interaction data from AWS SQS to generate a custom report PDF

```python
from hotel_coupon_app_package_alexandermamani.aws_services import SQSService, SQSPollingMessagesError,SQSClosingConnectionError
import environ
import json
from functools import partial


def handler_to_get_data_for_a_specific_hotelier_id(message, buffer_data, hotelier_coupon_ids):
    """
    Return True if the user interaction data is part of their own hotelier coupons, False otherwise.
    
    When True: Add the interaction user message to the buffer_data list and delete it from AWS SQS Queue.
    When False: keep the interaction user message to AWS SQS Queue.
    """
    message = json.loads(message['Body'])
    if message['coupon_id'] in hotelier_coupon_ids:
        buffer_data.append(message)
        return True
    else:
        return False


env = environ.Env()
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_REGION = env('AWS_REGION')
AWS_SQS_QUEUE_URL = env('AWS_SQS_QUEUE_URL')

buffer_processed_data = []

hotelier_coupon_ids = ["321-123-123123-123", 
                       "898-s-2-132-ad-213",
                       "f123-d2312-dwd-123"]

handler_with_buffer = partial(message_handler=handler_to_get_data_for_a_specific_hotelier_id, 
                              buffer_data=buffer_processed_data, 
                              hotelier_coupon_ids=hotelier_coupon_ids)

try:
    sqs_queue_instance = SQSService(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                    aws_region=AWS_REGION,
                                    aws_sqs_queue_url=AWS_SQS_QUEUE_URL)    
    sqs_queue_instance.poll_messages(handler_with_buffer, target_message_count=30)
    sqs_queue_instance.close()
    
    # Use buffer_processed_data to generate custom report PDF
    
except (SQSPollingMessagesError, SQSClosingConnectionError) as e:
    print("Error SQS", e)
```

#### Example of send user interaction data from AWS Lambda to AWS SQS Queue to 
 
```python
import json
from hotel_coupon_app_package_alexandermamani.aws_services import SQSService, SQSSendMessageError, SQSClosingConnectionError
import os


def lambda_handler(event, context):
    sqs_queue_instance = SQSService(aws_sqs_queue_url=os.environ['AWS_SQS_QUEUE_URL'])
    message = json.loads(event['body'])['message']

    data = {}
    data['coupon_id'] = message['coupon_id']
    data['action'] = message['action']
    data['user_profile_id'] = message['user_profile_id']
    data['country'] = message['country']
    data['date'] = message['date']

    try:
        sqs_queue_instance.send_message(data)
        sqs_queue_instance.close()
    except (SQSSendMessageError, SQSClosingConnectionError) as e:
        raise ("Error SQS", e)

    return {}
```