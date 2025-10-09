from aws_cdk import (
    aws_iam as iam,
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    CfnOutput
)
from constructs import Construct

class AppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, core_stack, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda function for planner (reasoning agent)
        planner_fn = _lambda.Function(
            self, "PlannerLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="planner.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": core_stack.table.table_name,
                "USE_BEDROCK": "true",
                "SENDER_EMAIL": "techwithsandhya1904@gmail.com"
            },
            timeout=Duration.seconds(60),
            memory_size=512
        )


        # Grant access to DynamoDB
        core_stack.table.grant_read_write_data(planner_fn)
        planner_fn.add_to_role_policy(core_stack.bedrock_policy)
        planner_fn.add_to_role_policy(iam.PolicyStatement(
            actions=[
                "ses:SendEmail",
                "ses:SendRawEmail"
            ],
            resources=["*"]
        ))

        # Create API Gateway endpoint
        api = apigw.LambdaRestApi(
            self, "CruiseAgentAPI",
            handler=planner_fn,
            proxy=False
        )

        quote = api.root.add_resource("quote")
        quote.add_method("POST")  # POST /quote

        health = api.root.add_resource("health")
        health.add_method("GET", apigw.MockIntegration(
            integration_responses=[{"statusCode": "200"}],
            request_templates={"application/json": '{"status": "ok"}'}
        ))
        
        # Output the api URL
        CfnOutput(self, "APIEndpoint", value=f"{api.url}quote")

        # Define the sender email function
        email_fn = _lambda.Function(
            self, "EmailLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="email_tool.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "SENDER_EMAIL": "techwithsandhya1904@gmail.com"
            },
            timeout=Duration.seconds(30),
            memory_size=256
        )

        email_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["ses:SendEmail", "ses:SendRawEmail"],
            resources=["*"]
        ))
