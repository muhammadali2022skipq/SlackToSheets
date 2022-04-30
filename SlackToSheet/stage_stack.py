from aws_cdk import (
    Stack,
    Stage
)
import aws_cdk as cdk_
from constructs import Construct
from .app_stack import SlackToSheetStack

class SlackToSheetStackStageStack(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.stage = SlackToSheetStack(self,"SlackToSheetStack")