import os

from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    Environment,
)
from constructs import Construct
from components import Node

REGIONS = {"origin": "us-east-1", "edge1": "us-west-1"}


class CDNStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Origin
        Node(
            self,
            "Origin",
        )

        # Edge
        Node(
            self,
            "Edge1",
        )
