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
    print("Launch Config created with name = {}".format(nome))

    return response

def create_modelo_exec(nome,id_imagem ,  secure_groups):
    client = boto3.client('ec2',region_name= "us-east-2")
    response = client.create_launch_template(
            LaunchTemplateName=nome,  
            LaunchTemplateData={ 
                'ImageId': id_imagem, 
                'InstanceType': 't2.micro', 
                'KeyName': 'Luca Cloud',    
                'SecurityGroupIds': [ 
                    secure_groups
                ], 
                # 'SecurityGroups': [  
                #     "security_group_projeto"  
                # ] 
                })
    print("Created Launch Template")
    return response["LaunchTemplate"]["LaunchTemplateId"]

def create_auto_scaling(loadbalacer_name,target_group_arn,autoscaling_name,lt_id):
    ec2Auto = boto3.client('autoscaling')
    response = ec2Auto.create_auto_scaling_group(
        AutoScalingGroupName= autoscaling_name,
        # LaunchConfigurationName= lauch_config_name,
        LaunchTemplate={
        'LaunchTemplateId': lt_id,
        'Version': '1'
        },
        # InstanceId=instance_id,
        MinSize=1,
        MaxSize=3,
        DesiredCapacity=1,
        # LoadBalancerNames=[
        #     loadbalacer_name
        # ],
        TargetGroupARNs=[
            target_group_arn
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
    print("Auto scaling group created with name {}". format(autoscaling_name))
    return response


# def add_scaling_policy(nome, autoscaling_name):
#     response = client.put_scaling_policy(
#     AutoScalingGroupName = autoscaling_name,
#     PolicyName= nome,
#     PolicyType='TargetTrackingScaling',
#     AdjustmentType='string',
#     MinAdjustmentStep=123,
#     MinAdjustmentMagnitude=123,
#     ScalingAdjustment=123,
#     Cooldown=123,
#     MetricAggregationType='string',
#     StepAdjustments=[
#         {
#             'MetricIntervalLowerBound': 123.0,
#             'MetricIntervalUpperBound': 123.0,
#             'ScalingAdjustment': 123
#         },
#     ],
#     EstimatedInstanceWarmup=123,
#     TargetTrackingConfiguration={
#         'PredefinedMetricSpecification': {
#             'PredefinedMetricType': 'ASGAverageCPUUtilization'|'ASGAverageNetworkIn'|'ASGAverageNetworkOut'|'ALBRequestCountPerTarget',
#             'ResourceLabel': 'string'
#         },
#         'CustomizedMetricSpecification': {
#             'MetricName': 'string',
#             'Namespace': 'string',
#             'Dimensions': [
#                 {
#                     'Name': 'string',
#                     'Value': 'string'
#                 },
#             ],
#             'Statistic': 'Average'|'Minimum'|'Maximum'|'SampleCount'|'Sum',
#             'Unit': 'string'
#         },
#         'TargetValue': 123.0,
#         'DisableScaleIn': True|False
#     },
#     Enabled=True|False)