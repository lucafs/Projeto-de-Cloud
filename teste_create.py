import boto.ec2
import time

conn = boto.ec2.connect_to_region('us-east-1')

# Enhanced creation now with the addition of 'user_data'

user_data_script = """#!/bin/bash
cd home/ubuntu/
sudo apt update
sudo apt install postgresql postgresql-contrib -y
sudo ufw allow 5432/tcp
sudo -u postgres psql -c "CREATE USER cloud WITH PASSWORD 'cloud'; "
sudo -u postgres createdb -O cloud tasks
sed -i "s/#listen_addresses = 'localhost'/listen_adresses = '*'/"  /etc/postgresql/10/main/postgresql.conf
sudo cat | sudo tee -a /etc/postgresql/10/main/pg_hba.conf <<EOF
host    all             all             0.0.0.0/0               trust
EOF

sudo systemctl restart postgresql"""

# Red Hat Enterprise Linux 6.4 (ami-7d0c6314)
new_reservation = conn.run_instances(
                        'ami-00ddb0e5626798373',
                        key_name='Luca Cloud',
                        instance_type='t2.micro',
                        security_groups=["sg-0b35197e850bfe265"],
                        user_data=user_data_script)
print ("New instance created.")

# Add a Name to the instance, then loop to wait for it to be running.
instance = new_reservation.instances[0]
while instance.state == u'pending':
    print ("Instance state: %s" % instance.state)
    time.sleep(10)
    instance.update()

print ("Instance state: %s" % instance.state)
print ("Public dns: %s" % instance.public_dns_name)