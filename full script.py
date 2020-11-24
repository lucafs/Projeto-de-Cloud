import boto3
from launch_instances import *
from security_groups import create_SG
from load_balancer import delete_instance_by_id
ec2_reg1 = boto3.client('ec2',region_name= "us-east-1")
ec2_reg2 = boto3.client('ec2',region_name= "us-east-2")

#Cria o security group nas duas instancias se não existir ainda
id_security_banco = create_SG("security_group_projeto" , "us-east-1")
id_security_orm = create_SG("security_group_projeto" , "us-east-2")

#Cria o banco de dados
id_inst_banco = launch_instances(1,user_data_postgress,1, id_security_banco)

#Pega o Ip do banco de dados e cria instancia da ORM
pub_ip_banco = ec2_reg1.describe_instances(InstanceIds=[id_inst_banco])['Reservations'][0]['Instances'][0]['PublicIpAddress']
id_inst_orm =launch_instances(1,user_data_django.format(pub_ip_banco),2,id_security_orm)
#Cria imagem da instancia ORM e deleta a instancia
create_image(id_inst_orm,"Imagem ORM", "us-east-2")
delete_instance_by_id(id_inst_orm, "us-east-2")

