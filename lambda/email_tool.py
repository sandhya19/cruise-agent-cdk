import boto3
import os

ses = boto3.client("ses", region_name="eu-central-1")
SENDER = os.environ.get("SENDER_EMAIL", "techwithsandhya1904@gmail.com")

def send_email(to_address, subject, message):
    try:
        response = ses.send_email(
            Source=SENDER,
            Destination={"ToAddresses": [to_address]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": message}}
            }
        )
        return {"status": "sent", "message_id": response["MessageId"]}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
