from aws_cdk import Stack, aws_ec2 as ec2, CfnOutput
from constructs import Construct
from enum import Enum

# TODO: Check security group settings!!

ORIGIN_HTML = "<h1>Hello from the origin</h1>"

NODE_NGINX_CONF = """
proxy_cache_path /var/cache/nginx/cdn levels=1:2 keys_zone=cdn_cache:10m max_size=1g inactive=60m use_temp_path=off;
 
server {
    listen 80 default_server;
 
    location / {
        proxy_pass http://__ORIGIN__;
        proxy_cache cdn_cache;
        proxy_cache_valid 200 301 302 10m;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503;
        add_header X-Cache-Status $upstream_cache_status;
    }
}
"""


class NodeType(Enum):
    ORIGIN = 0
    EDGE = 1


class Node(Stack):
    cdn_origin_ip: str

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        type: NodeType,
        total_nodes: int = 1,
        *,
        vpc: ec2.Vpc | None = None,
        sec_group: ec2.SecurityGroup | None = None,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC Setup
        if vpc is None:
            vpc = self._new_vpc(type)

        # Security Group Setup
        if sec_group is None:
            sec_group = self._new_security_group(type, vpc)

        user_data: ec2.UserData = self._get_user_data(type)
        subnets = vpc.public_subnets

        for i in range(total_nodes):
            # EC2 Instance
            instance = ec2.Instance(
                self,
                f"{type.name}_EC2",
                vpc=vpc,
                vpc_subnets=ec2.SubnetSelection(subnets=[subnets[i % len(subnets)]]),
                security_group=sec_group,
                instance_type=ec2.InstanceType.of(
                    ec2.InstanceClass.T3, ec2.InstanceSize.MICRO
                ),
                machine_image=ec2.MachineImage.latest_amazon_linux2023(),
                user_data=user_data,
            )
            # Output EC2 IP
            CfnOutput(
                self,
                "InstancePublicIp",
                value=instance.instance_public_ip,
            )
            # Set origin ip
            if type is NodeType.ORIGIN:
                Node.cdn_origin_ip = instance.instance_public_ip

    def _new_vpc(self, type: NodeType) -> ec2.Vpc:
        return ec2.Vpc(
            self,
            f"{type.name}_VPC",
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24
                )
            ],
        )

    def _new_security_group(self, type: NodeType, vpc: ec2.Vpc) -> ec2.SecurityGroup:
        new_group = ec2.SecurityGroup(
            self,
            f"{type.name}_SG",
            vpc=vpc,
            description="Allow SSH access",
            allow_all_outbound=True,
        )

        new_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "Allow SSH",
        )

        new_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            f"Allow HTTP",
        )

        return new_group

    def _get_user_data(self, type: NodeType) -> ec2.UserData:
        user_data = ec2.UserData.for_linux()
        if type == NodeType.EDGE:
            try:
                conf = NODE_NGINX_CONF.replace("__ORIGIN__", Node.cdn_origin_ip)
                user_data.add_commands(
                    "dnf install -y nginx",
                    "mkdir -p /var/cache/nginx/cdn && chown nginx:nginx /var/cache/nginx/cdn",
                    f"cat > /etc/nginx/conf.d/cdn.conf << 'EOF'\n{conf}\nEOF",
                    "sed -i '/^\\s*server {/,/^\\s*}/d' /etc/nginx/nginx.conf || true",
                    "systemctl enable --now nginx",
                )
            except AttributeError as e:
                print("Likely did not create the origin stack before an edge.")
                raise
        else:
            user_data.add_commands(
                "dnf install -y nginx",
                f"echo '{ORIGIN_HTML}' > /usr/share/nginx/html/index.html",
                "systemctl enable --now nginx",
            )
        return user_data
