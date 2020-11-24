import boto3

def create_LaunchConfig(nome,AMI_ID, security_group_id ,region):
    client = boto3.client('autoscaling', region_name = region)
    response = client.create_launch_configuration(
    LaunchConfigurationName= nome,
    ImageId= AMI_ID,
    SecurityGroups=[
        security_group_id
    ],
    InstanceType='t2.micro',
    InstanceMonitoring={
        'Enabled': True
    })
    return response

def create_auto_scaling(loadbalacer_name, autoscaling_name, lauch_config_name):
    ec2Auto = boto3.client('autoscaling')
    response = ec2Auto.create_auto_scaling_group(
        AutoScalingGroupName= autoscaling_name,
        LaunchConfigurationName= lauch_config_name,
        MinSize=1,
        MaxSize=3,
        DesiredCapacity=1,
        LoadBalancerNames=[
            loadbalacer_name
        ],
        VPCZoneIdentifier ='subnet-88de86e0,subnet-9bd42dd7,subnet-d53badaf',
        # Tags=[
        #     {
        #         'ResourceId': 'string',
        #         'ResourceType': 'string',
        #         'Key': 'string',
        #         'Value': 'string',
        #         'PropagateAtLaunch': True|False
        #     },
        # ],
    )
    return response


# response = create_LaunchConfig("teste","ami-0e45e8235ef3e8d33","sg-0b3f8e9f355199f3f","us-east-2")

response = create_auto_scaling("testeLB","teste_auto2","teste")
print(response)