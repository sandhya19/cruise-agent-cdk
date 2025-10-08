import json
import boto3
import os
import uuid
from email_tool import send_email
from quote_tool import generate_quote


table_name = os.environ.get("TABLE_NAME")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(table_name)

def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        query = body.get("query", "Plan a cruise itinerary")

        result = {}
        try:
            bedrock = boto3.client("bedrock-runtime", region_name="eu-central-1")
            model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
            # system_prompt = (
            #     "You are a cruise holiday planner. "
            #     "Return response strictly in valid JSON with fields: "
            #     "destination, cruise_duration, hotel_stay, estimated_price, description."
            # )

            payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 200,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "You are a cruise holiday planner. "
                                    "Always respond ONLY in valid JSON with fields: "
                                    "destination, cruise_duration, hotel_stay, estimated_price, description. "
                                    "If unsure, leave fields empty. "
                                    f"User request: {query}"
                                )
                            }
                        ]
                    }
                ]
            }

            response = bedrock.invoke_model(
                modelId=model_id,
                body=json.dumps(payload)
            )

            response_body = json.loads(response["body"].read())
            result_text = response_body["content"][0]["text"]

            # Step 2: Try parsing JSON safely
            try:
                result_json = json.loads(result_text)
            except json.JSONDecodeError:
                result_json = {"description": result_text}

            result = result_json

            # Step 3: Generate quote
            quote = generate_quote(
                destination=result.get("destination", "Singapore"),
                nights=7,
                adults=2,
                children=1
            )
            result["estimated_price"] = quote["estimated_price"]

            # Step 4: Compose and send email
            email_text = (
                f"Destination: {quote['destination']}\n"
                f"Nights: {quote['nights']}\n"
                f"Estimated Price: {quote['estimated_price']}\n"
                f"Description: {result.get('description', '')}"
            )

            send_email("sand.ash19@gmail.com", "Your Cruise & Stay Quote", email_text)

        except Exception as e:
            result = {"mock_result": f"Mock itinerary for: {query}", "error": str(e)}

        # Save to DynamoDB
        record = {
            "id": str(uuid.uuid4()),
            "query": query,
            "result": result
        }
        table.put_item(Item=record)

        return {
            "statusCode": 200,
            "body": json.dumps({"result": result})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }