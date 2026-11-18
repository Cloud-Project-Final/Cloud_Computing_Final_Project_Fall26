#!/usr/bin/env python3
import os

import aws_cdk as cdk

# from init_cdk.init_cdk_stack import InitCdkStack
from init_cdk.cdn_node import Node

REGIONS = {"origin": "us-east-1", "edge1": "us-west-1"}

app = cdk.App()
# InitCdkStack(
#     app,
#     "InitCdkStack",
#     # If you don't specify 'env', this stack will be environment-agnostic.
#     # Account/Region-dependent features and context lookups will not work,
#     # but a single synthesized template can be deployed anywhere.
#     # Uncomment the next line to specialize this stack for the AWS Account
#     # and Region that are implied by the current CLI configuration.
#     # env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
#     # Uncomment the next line if you know exactly what Account and Region you
#     # want to deploy the stack to. */
#     # env=cdk.Environment(account='123456789012', region='us-east-1'),
#     # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
# )

# Origin
Node(
    app,
    "Origin",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=REGIONS["origin"]
    ),
)

# Edge
Node(
    app,
    "Edge1",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=REGIONS["edge1"]
    ),
)

app.synth()
