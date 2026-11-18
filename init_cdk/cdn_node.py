from aws_cdk import Stack, aws_ec2 as ec2, CfnOutput
from constructs import Construct


class Node(Stack):

    def __init__(
        self,
        vpc: ec2.Vpc | None,
        sec_group: ec2.SecurityGroup | None,
        scope: Construct,
        construct_id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC Setup
        if vpc is None:
            vpc = self._new_vpc()

        # Security Group Setup
        if sec_group is None:
            sec_group = self._new_security_group(vpc)

        # EC2 Instance
        instance = ec2.Instance(
            self,
            "WebInstance",
            vpc=vpc,
            security_group=sec_group,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3, ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
        )

        # Output EC2 IP
        CfnOutput(
            self,
            "InstancePublicIp",
            value=instance.instance_public_ip,
        )

    def _new_vpc(self) -> ec2.Vpc:
        return ec2.Vpc(
            self,
            "AppVpc",
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                )
            ],
        )

    def _new_security_group(self, vpc: ec2.Vpc) -> ec2.SecurityGroup:
        new_group = ec2.SecurityGroup(
            self,
            "InstanceSG",
            vpc=vpc,
            description="Allow SSH access",
            allow_all_outbound=True,
        )

        new_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "Allow SSH",
        )

        return new_group
