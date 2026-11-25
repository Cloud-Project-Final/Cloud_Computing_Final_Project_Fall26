import aws_cdk as cdk
from aws_cdk import (
    aws_ec2 as ec2,
    aws_efs as efs,
)
from constructs import Construct


class Storage(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.IVpc,
        ec2_instance: ec2.Instance,
        replication_region: str,
    ) -> None:
        super().__init__(scope, construct_id)
