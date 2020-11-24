import boto3
def delete_instance_by_id(instance_id, region):
    ec2 = boto3.resource('ec2',region_name= region)
    resp = ec2.instances.filter(InstanceIds=[instance_id]).terminate()
    print ("Instace {} was terminated".format(instance_id))
    return resp

def create_target_G (nome):
    ec2lb = boto3.client('elbv2')
    ec2 = boto3.client('ec2',region_name= "us-east-2")

    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    response = ec2lb.create_target_group(
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
    return response

def create_LB(nome, security_group):
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
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        }])
    return response["LoadBalancers"][0]["LoadBalancerArn"] , nome ,  res







# response = create_LaunchConfig("teste","ami-0e45e8235ef3e8d33","sg-0b3f8e9f355199f3f","us-east-2")
# arn,nome ,res = create_LB("testeLB","sg-0b3f8e9f355199f3f")
# print(res)
#arn:aws:elasticloadbalancing:us-east-2:671559748688:loadbalancer/app/testeLB/18fd6c955bf21e03

res = create_target_G("teste")
print(res)