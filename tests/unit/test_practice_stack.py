import aws_cdk as core
import aws_cdk.assertions as assertions

from practice.practice_stack import PracticeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in practice/practice_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PracticeStack(app, "practice")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
