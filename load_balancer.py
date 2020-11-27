import boto3
from launch_instances import launch_instances , user_data_django
def delete_instance_by_id(instance_id, region):
    ec2 = boto3.resource('ec2',region_name= region)
    resp = ec2.instances.filter(InstanceIds=[instance_id]).terminate()
    print ("Instace {} was terminated".format(instance_id))
    return resp

def create_target_G(nome ,id_one,id_two,id_three):
    ec2lb = boto3.client('elbv2')
    ec2 = boto3.client('ec2',region_name= "us-east-2")

    res = ec2.describe_vpcs()
    vpc_id = res.get('Vpcs', [{}])[0].get('VpcId', '')

    response_create = ec2lb.create_target_group(
    Name = nome,
    Protocol='HTTP',
    Port=8080,
    VpcId=vpc_id,

    TargetType='instance',
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        }])
    targetGarn = response_create["TargetGroups"][0]["TargetGroupArn"]
    response_register = ec2lb.register_targets(
    TargetGroupArn = targetGarn,
    Targets=[
        {
            'Id': id_one,
            'Port': 8080,
        },
        {
            'Id': id_two,
            'Port': 8080,
        },
        {
            'Id': id_three,
            'Port': 8080,
        },
    ]
    )
    print("Target Group criado com a arn ={} ".format(response_create["TargetGroups"][0]["TargetGroupArn"]))
    return response_create["TargetGroups"][0]["TargetGroupArn"]

def create_LB(nome, security_group, target_group):
    ec2lb = boto3.client('elbv2')

    #Cria LB
    response = ec2lb.create_load_balancer(
        Name = nome,
        Subnets = [
            'subnet-88de86e0',
            'subnet-d53badaf',
            'subnet-9bd42dd7',

        ],
        SecurityGroups=[security_group],
        Scheme='internet-facing',
        Tags=[
            {
                'Key': 'string',
                'Value': 'string'
            },
        ],
        Type='application',
        IpAddressType='ipv4',
    )
    res = ec2lb.create_listener(
    LoadBalancerArn=response["LoadBalancers"][0]["LoadBalancerArn"],
    Protocol='HTTP',
    Port=80,
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': target_group,
        }],
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        }])
    print("load balacer criado com arn = {0} e nome ={1}".format(response["LoadBalancers"][0]["LoadBalancerArn"], nome))
    return response["LoadBalancers"][0]["LoadBalancerArn"] , nome ,  res







# response = create_LaunchConfig("teste","ami-0e45e8235ef3e8d33","sg-0b3f8e9f355199f3f","us-east-2")
# arn,nome ,res = create_LB("testeLB","sg-0b3f8e9f355199f3f")
# print(res)
#arn:aws:elasticloadbalancing:us-east-2:671559748688:loadbalancer/app/testeLB/18fd6c955bf21e03

# resp1 =launch_instances(1,user_data_django, 2,"sg-0b3f8e9f355199f3f")
# resp2 =launch_instances(1,user_data_django, 2,"sg-0b3f8e9f355199f3f")
# resp3 =launch_instances(1,user_data_django, 2,"sg-0b3f8e9f355199f3f")

# res = create_target_G("testefinal5", "i-0c67e3cc2db30b513","i-0978f067d3451bab2","i-09e0d93611fd3a85a")
# print(create_LB("testeLB4","sg-0b3f8e9f355199f3f",res))



# res = create_target_G("testefinal", "i-0bf9d81e815d02b60","i-0a3c8447c70fcd1cd","i-0eef001a19cb263ac")
#  arn,nome ,res = create_LB("testeLB","sg-0b3f8e9f355199f3f")
# print(create_LB("testeLB2","sg-0b3f8e9f355199f3f",res))
# print(res)