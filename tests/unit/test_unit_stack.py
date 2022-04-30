import aws_cdk as core
import aws_cdk.assertions as assertions

from SlackToSheet.app_stack import SlackToSheetStack

# example tests. To run these tests, uncomment this file along with the example
# resource in practice/practice_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SlackToSheetStack(app, "SlackToSheetStack")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
