# Cloud deploying script using boto3.

## How to run:

First you need to put your credentials using the following command.
```
aws configure
```
If you don't have boto3 installed.
```
pip install boto3
```
Now you just run the full script code.
```
python full_script.py
```

## What does it do?

### This code releases a full aplication with autoscalling and a loadbalancer, other than that we have the a ORM application using django in one AWS region(use-east-1) and a database in another(use-east-2).
----------------------------
### When you run the full script:

    -  Create two different security groups in both regions.
    -  Launch 3 instances of the ORM load balancer and 1 for the database.
    -  Create target group, load balancer and image from ORM instance.
    -  Terminates all 3 instances from ORM.
    -  Finally it creates the Auto Scalling Load Balancer connected to the database.