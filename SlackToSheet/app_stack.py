from aws_cdk import (
    aws_apigateway as api_,
    Stack,
    aws_sqs as sqs_,
    aws_lambda as lambda_,
    RemovalPolicy,
    Duration,
)
from constructs import Construct


class SlackToSheetStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ProducerLambda_Function = self.create_lambda(
            "SlackToSheets_ProducerLambda",
            './resources',
            'ProducerLambda.handler_name',
        )

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/README.html
        # Amazon API Gateway is a fully managed service that makes it easy for developers to publish, maintain, monitor, and secure APIs at any scale.

        api = api_.LambdaRestApi(
            self,
            "SlackToSheets_SlackUserDataReceivingAPI",
            handler=ProducerLambda_Function,
        )
        api.apply_removal_policy(RemovalPolicy.DESTROY)

        printData = api.root.add_resource("slackuserdata")
        printData.add_method("GET")
        printData.add_method("POST")

        user_data_queue = sqs_.Queue(
            self,
            "SlackToSheets_SlackUserDataQueue",
            content_based_deduplication=True,
            fifo=True,
            removal_policy=RemovalPolicy.DESTROY,
        )
        user_data_queue.grant_send_messages(ProducerLambda_Function)
        ProducerLambda_Function.add_environment(key="SQS_Queue_Name",value=user_data_queue.queue_name)
        

    def create_lambda(self, id, asset, handler):
        lambda_Function = lambda_.Function(
            self,
            id=id,
            code=lambda_.Code.from_asset(asset),
            handler=handler,
            runtime=lambda_.Runtime.PYTHON_3_6,
            timeout=Duration.seconds(30),
        )
        lambda_Function.apply_removal_policy(RemovalPolicy.DESTROY)
        return lambda_Function