from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_iam as iam,
    RemovalPolicy
)
from constructs import Construct

class CoreStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB table for logs
        self.table = dynamodb.Table(
            self, "AgentLogs",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Static site bucket
        self.site_bucket = s3.Bucket(
            self, "StaticSiteBucket",
            website_index_document="index.html",
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(block_public_acls=False, block_public_policy=False),
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Common policy for Bedrock + SES
        self.bedrock_policy = iam.PolicyStatement(
            actions=[
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "ses:SendEmail",
                "ses:SendRawEmail"
            ],
            resources=["*"]
        )