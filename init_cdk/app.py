#!/usr/bin/env python3
import os

from aws_cdk import (
    # Duration,
    Stack,
    App,
    Environment,
)
from constructs import Construct
from components import Node, NodeType

REGIONS = {"origin": "us-east-1", "edge1": "us-west-1"}

app = App()
account = os.getenv("CDK_DEFAULT_ACCOUNT")

# Origin
Node(
    app,
    "Origin",
    NodeType.ORIGIN,
    env=Environment(account=account, region=REGIONS["origin"]),
)

Node(
    app,
    "WestEdge",
    NodeType.EDGE,
    env=Environment(account=account, region=REGIONS["edge1"]),
)


app.synth()
