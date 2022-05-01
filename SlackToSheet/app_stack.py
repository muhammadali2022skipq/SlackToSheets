from aws_cdk import (
    aws_apigateway as api_,
    Stack,
    aws_sqs as sqs_,
    aws_lambda as lambda_,
    aws_lambda_event_sources as event_,
    aws_iam as iam_,
    RemovalPolicy,
    Duration,
)
from constructs import Construct


class SlackToSheetStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lamdaRoles = self.create_lamba_role()
        ProducerLambda_Function = self.create_lambda(
            "SlackToSheets_ProducerLambda",
            './resources',
            'ProducerLambda.handler_name',
            lamdaRoles
        )

        ConsumerLambda_Function = self.create_lambda(
            "SlackToSheets_ConsumerLambda",
            './resources',
            'ConsumerLambda.handler_name',
            lamdaRoles
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
            visibility_timeout=Duration.seconds(60),
            delivery_delay=Duration.seconds(30),
            removal_policy=RemovalPolicy.DESTROY,
        )

        user_data_queue.grant_send_messages(ProducerLambda_Function)
        user_data_queue.grant_consume_messages(ConsumerLambda_Function)
        ProducerLambda_Function.add_environment(
            key="SQS_Queue_Name", value=user_data_queue.queue_name)
        ConsumerLambda_Function.add_event_source(
            event_.SqsEventSource(user_data_queue))

    def create_lambda(self, id, asset, handler, roles):
        lambda_Function = lambda_.Function(
            self,
            id=id,
            code=lambda_.Code.from_asset(asset),
            handler=handler,
            runtime=lambda_.Runtime.PYTHON_3_6,
            timeout=Duration.seconds(30),
            role=roles,
        )
        lambda_Function.apply_removal_policy(RemovalPolicy.DESTROY)
        return lambda_Function

    def create_lamba_role(self):
        lambda_role = iam_.Role(
            self,
            "SlackToSheets_IAM_Roles",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[

                iam_.ManagedPolicy.from_aws_managed_policy_name(
                    "SecretsManagerReadWrite"),

            ],
        )
        lambda_role.apply_removal_policy(RemovalPolicy.DESTROY)
        return lambda_role
