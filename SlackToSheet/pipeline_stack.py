from aws_cdk import (
    Stack,
    pipelines as pipelines_,
    aws_codepipeline_actions as pipeline_actions_
)
import aws_cdk as cdk_
from constructs import Construct
from .stage_stack import SlackToSheetStackStageStack


class SlackToSheetStackPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines.html

        # Source step (Github)
        source = self.createSource(
            repo="muhammadali2022skipq/SlackToSheets",
            repo_branch="main",
            auth_key="muhammadali2022skipq_github_token",
            trigger='POLL',
        )

        # Build step
        # Runs the shellstep commands to install the necessary packages and build the project
        synth = self.createShellSteps(
            id="SynthStep",
            source=source,
            commands_list=[
                "pip install -r requirements.txt",
                "pip install google-api-python-client oauth2client --target=resources/",
                "npm install -g aws-cdk",
                "cdk synth",
            ],
            have_output=True,
        )
        # Shell step to install the necessary package for testing and running the unit tests
        test_step = self.createShellSteps(
            id="Unit_Test_Step",
            source=source,
            commands_list=[
                "pip install pytest",
                "pip install -r requirements.txt",
                "npm install -g aws-cdk",
                "python -m pytest"
            ],
            have_output=False,
        )

        # Deploy Step to deploy the Cloudformation template
        slacktosheet_pipeline = pipelines_.CodePipeline(
            self,
            id="SlackToSheetStackPipeline",
            synth=synth
        )

        # # Created a instance of Stage Stack
        beta_stage = self.createStage(id="beta")

        # Created a instance of Stage Stack
        # prod_stage = self.createStage(id="prod")

        # Adding beta and prod stage in our pipeline
        slacktosheet_pipeline.add_stage(
            beta_stage,
            pre=[test_step]
        )

        # slacktosheet_pipeline.add_stage(
        #     prod_stage,
        #     pre=pipelines_.Step.sequence(
        #         [pipelines_.ManualApprovalStep("Deploy_To_Production")])
        # )

    # Function to create source
    def createSource(self, repo, repo_branch, auth_key, trigger):
        create_source = pipelines_.CodePipelineSource.git_hub(
            repo_string=repo,
            branch=repo_branch,
            authentication=cdk_.SecretValue.secrets_manager(auth_key),
            trigger=pipeline_actions_.GitHubTrigger(trigger)
        )
        return create_source
    # Function to create ShellStep

    def createShellSteps(self, id, source, commands_list, have_output: bool):
        output = "cdk.out"if have_output else None
        steps = pipelines_.ShellStep(
            id=id,
            input=source,
            commands=commands_list,
            primary_output_directory=output,
        )
        return steps
    # Function to create stage

    def createStage(self, id):
        stage = SlackToSheetStackStageStack(
            self,
            id,
            env=cdk_.Environment(
                account='315997497220',
                region='us-east-2'
            )
        )
        return stage
