import boto3
from security_groups import create_SG
from botocore.exceptions import ClientError
import time


def launch_instances(number, user_data, region_number, security_group):
    if region_number == 1:
        instances_resource = boto3.resource('ec2', 'us-east-1')
        imageAMI = 'ami-00ddb0e5626798373'
        
        # imageAMI = 'ami-0885b1f6bd170450c'

    elif region_number == 2:
        instances_resource = boto3.resource('ec2', 'us-east-2')
        imageAMI = 'ami-0dd9f0e7df0f0a138'
    else:
        return "Region not autorized."
    # create a new EC2 instance
    response_instances = instances_resource.create_instances(
        ImageId=imageAMI,
        InstanceType='t2.micro',
        MinCount=number,
        MaxCount=number,
        SecurityGroupIds=[security_group],
        KeyName='Luca Cloud',
        UserData=user_data
    )
    instance_id = response_instances[0].instance_id
    print("Created instance with the id = {} in region {}".format(instance_id, region_number))
    return instance_id

def create_image(instance_id , nameImg , region):
    ec2 = boto3.client('ec2',region_name= region)
    print("Waiting for instances to run")
    waiter = ec2.get_waiter('instance_status_ok')
    waiter.wait(
    InstanceIds=[
        instance_id])
    try:
        response = ec2.create_image(InstanceId= instance_id, Name = nameImg)   
        image_id = response['ImageId'] 
        waiter = ec2.get_waiter('image_available')
        print("Wating for AMI to be ready ... This may take a while")
        waiter.wait(
            ImageIds=[
                image_id
            ]
        )
        print("AMI created with id = {}".format(image_id))
        return image_id
    except ClientError as e:
        print("AMI with this name aready exist")
        response = ec2.describe_images(Owners=['self'])
        image_id= response["Images"][0]["ImageId"]
        print("Imagem com ID {}".format(image_id))
        return image_id

    

user_data_postgress = """#!/bin/bash
cd ..
cd home/ubuntu/
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo -u postgres psql -c "CREATE USER cloud WITH PASSWORD 'cloud'; "
sudo -u postgres createdb -O cloud tasks
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/"  /etc/postgresql/10/main/postgresql.conf
echo "host    all             all             0.0.0.0/0              trust" >> /etc/postgresql/10/main/pg_hba.conf
ufw allow 5432/tcp
sudo systemctl restart postgresql"""

user_data_django = '''#!/bin/bash
cd ..
cd /home/ubuntu/
sudo apt update
git clone https://github.com/lucafs/tasks.git
sed -i "s/'HOST': '3.82.252.173',/'HOST': '{}',/"  /home/ubuntu/tasks/portfolio/settings.py
cd tasks/
./install.sh
reboot
'''



# create_image("i-0a18fa42de33c9a64","teste", "us-east-2")
#id_security = create_SG("security_group_projeto" , "us-east-1")
# print(id_security)

# resp = launch_instances(1,user_data_postgress,1, "sg-055f2f83344e07db2")
# print(resp)

# id_inst_orm =launch_instances(1,user_data_django.format("18.204.6.154"), 2,"sg-0b3f8e9f355199f3f")
# create_image("i-0fedd9e82b0f2803d","sla","us-east-2")

# resp2 =launch_instances(1,user_data_django, 2,"sg-0b3f8e9f355199f3f")
# print(resp2)

# id_inst_orm =launch_instances(1,user_data_django.format("54.152.56.157"),2,"sg-0b3f8e9f355199f3f")


#LEMBRAR DE FILTRAR POR NOME
# filters = [{  
#     'Name': 'Image',
#     'Values': ['vamo ae']
#     }]
# ec2 = boto3.client('ec2',region_name= "us-east-1")

# response = ec2.describe_images(Owners=['self'])
# print(response)
# print(response["Images"][0]["ImageId"])

