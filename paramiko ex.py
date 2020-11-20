import boto3
import botocore
import paramiko

key = paramiko.RSAKey.from_private_key_file("/home/lucafs/key_lfs")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect/ssh to an instance

try:
    # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
    client.connect(hostname='54.91.94.101', username="ubuntu", pkey=key)
    # Execute a command(cmd) after connecting/ssh to an instance
    (stdin, stdout, stderr)= client.exec_command('sudo apt update',timeout=4)

    (stdin, stdout, stderr) = client.exec_command('sudo apt install postgresql postgresql-contrib -y')
    for line in stdout.readlines():
        print (line)
#    print(stdout)

    # close the client connection once the job is done
    client.close
    

except:
    print("error")