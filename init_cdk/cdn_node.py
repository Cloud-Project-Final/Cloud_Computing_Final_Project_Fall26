from aws_cdk import Stack, aws_ec2 as ec2, CfnOutput
from constructs import Construct


class Node(Stack):

    def __init__(
        self,
        vpc: ec2.Vpc,
        sec_group: ec2.SecurityGroup,
        scope: Construct,
        construct_id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC Setup
        if vpc is None:
            vpc = ec2.Vpc(
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

        # Security Group Setup
        if sec_group is None:
            sec_group = ec2.SecurityGroup(
                self,
                "InstanceSG",
                vpc=vpc,
                description="Allow SSH access",
                allow_all_outbound=True,
            )

            sec_group.add_ingress_rule(
                ec2.Peer.any_ipv4(),
                ec2.Port.tcp(22),
                "Allow SSH",
            )

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
