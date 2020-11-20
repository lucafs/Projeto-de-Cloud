import boto3
from security_groups import create_SG

def launch_instances(number, user_data , region_number, security_group):
    if region_number == 1:
        instances_resource = boto3.resource('ec2', 'us-east-1')
        imageAMI = 'ami-00ddb0e5626798373'
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
    instance_id =response_instances[0].instance_id
    print(instance_id)
    return instance_id


user_data_postgress = """#!/bin/bash
cd home/ubuntu/
sudo apt update
echo "a" >> log.txt
sudo apt install postgresql postgresql-contrib -y
echo "b" >> log.txt
ufw allow 5432/tcp
echo "c" >> log.txt
sudo -u postgres psql -c "CREATE USER cloud WITH PASSWORD 'cloud'; "
echo "d" >> log.txt
sudo -u postgres createdb -O cloud tasks
echo "e" >> log.txt
sed -i "s/#listen_addresses = 'localhost'/listen_adresses = '*'/"  /etc/postgresql/10/main/postgresql.conf
echo "f" >> log.txt
cat | sudo tee -a /etc/postgresql/10/main/pg_hba.conf <<EOF
host    all             all             0.0.0.0/0               trust
EOF


echo "g" >> log.txt
sudo systemctl restart postgresql
echo "h" >> log.txt"""

user_data_django ='''#!/bin/bash
sudo apt update
git clone https://github.com/lucafs/tasks.git
sed -i "s/'HOST': '3.82.252.173',/'HOST': '35.171.3.155',/"  /tasks/portfolio/settings.py
cd tasks/
./install.sh
sudo reboot'''

#def create_image(instance_id , name)
 #   ec2.create_image(InstanceId=instance_id, Name="abc").
  #  return()


#id_security = create_SG("security_group_projeto" , "us-east-1")
#print(id_security)

resp = launch_instances(1,user_data_postgress,1, "sg-0b35197e850bfe265")
print(resp)


#launch_instances(1,user_data_django, 2,"sg-0b3f8e9f355199f3f")
#i-0fec631225b3a40b6  BANCO
#i-03d449bd509473ee7  ORM

