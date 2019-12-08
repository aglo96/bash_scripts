import boto3
import json
import pprint
import time
from botocore.exceptions import ClientError 
from fabric import Connection
import argparse


# def configure_aws(accesskey, secretkey):
#     c = Connection("localhost")
#     c.local("echo asdad")
#     c.local("aws configure")


def list_ec2_instances():
    ec2 = boto3.client('ec2')
    instances = {}
    res = ec2.describe_instances()
    pprint.pprint(res['Reservations'][4]) #has 5 diff instances
    # for r in res['Reservations']:
    #     for ins in r['Instances']:
    #         if ins['State']['Name'] == 'running':
    #             instances[ins['InstanceId']] = ins['PublicIpAddress']
    # print(instances)
 
def name_ec2_instance():
    ec2 = boto3.client('ec2')
    res = ec2.describe_instances()
    for r in res['Reservations']:
        for ins in r['Instances']:
            if ins['InstanceId'] == "i-006b53dce5fb1d1c6":
                print("Hello")
                ec2.create_tags(Resources=['i-006b53dce5fb1d1c6'], Tags=[{'Key': 'Name', 'Value': 'flask_webserver'}])
 
 
 
def create_security_group(security_group_name):
    ec2 = boto3.client('ec2')
    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
    try:
        response = ec2.create_security_group(GroupName=security_group_name,
                                            Description='DESCRIPTION',
                                            VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
    except ClientError as e:
         print(e)
         return
    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 0,
             'ToPort': 65535,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
    print('Ingress Successfully Set %s' % data)
 
 

def create_ec2_instances(security_group_name):
    ec2 = boto3.resource('ec2')

    #create 4 ec2 instances for production system
    res = ec2.create_instances(
        ImageId='ami-061eb2b23f9f8839c',
        MinCount=4,
        MaxCount=4,
        InstanceType='t2.small',
        KeyName='test1',
        SecurityGroups=[security_group_name]
    )
    ec2_id_list = []
    for i in res:
        ec2_id_list.append(i.instance_id)
    
    ec2_instances["mysql"] = ec2_id_list[0]
    ec2_instances["mongodb"] = ec2_id_list[1]
    ec2_instances["backend"] = ec2_id_list[2]
    ec2_instances["frontend"] = ec2_id_list[3]
    
    print(ec2_id_list)
    print(ec2_instances)
    print("Waiting for instances to be ready")
    
    client = boto3.client('ec2')
    waiter = client.get_waiter('instance_running')
    waiter.wait(
    InstanceIds=ec2_id_list,
    WaiterConfig={
        'Delay': 5,
        'MaxAttempts': 50
    }
    )  
    
    print("instances are running")
    
    # Obtain public dns of the newly created instances
    running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])
    for instance in running_instances:
        if instance.instance_id == ec2_instances["mysql"]:
            ec2_public_dns["mysql"] = [instance.public_dns_name, instance.public_ip_address]
        elif instance.instance_id == ec2_instances["mongodb"]:
            ec2_public_dns["mongodb"] = [instance.public_dns_name, instance.public_ip_address]
        elif instance.instance_id == ec2_instances["backend"]:
            ec2_public_dns["backend"] = [instance.public_dns_name, instance.public_ip_address]
        elif instance.instance_id == ec2_instances["frontend"]:
            ec2_public_dns["frontend"] = [instance.public_dns_name, instance.public_ip_address]
    




def write_to_file(ec2_public_dns):
    with open("ec2InstancesProductionSystem.txt", "w") as outputFile:
        for instance_type in ec2_public_dns:
            outputFile.write(f"{instance_type} {ec2_public_dns[instance_type][0]} {ec2_public_dns[instance_type][1]}\n")    


    
def setup_ec2_instance(server_type, ec2_public_dns, keypair):
    print(keypair)
    dns = ec2_public_dns[server_type][0]
    print(dns)
    c = Connection(host = dns, user='ubuntu', connect_kwargs={
        "key_filename": keypair
    })
    c.run('git clone https://github.com/aglo96/bash_scripts.git') #to download bash script
    if server_type == "backend" or server_type == "frontend":
        c.run('git clone https://github.com/skimkoh/bigdata-goodreads.git')
        c.put('ec2InstancesProductionSystem.txt', 'bigdata-goodreads/')
    with c.cd('~/bash_scripts'):
        if server_type == "mysql":
            c.run('bash installmysql.sh')
        elif server_type == "mongodb":
            c.run('bash installmongo.sh')
        elif server_type == "backend":
            c.run('bash setupbackend.sh')
        elif server_type == "frontend":
            c.run('bash setupfrontend.sh')


def terminate_ec2_instances():
    ec2list = []
    statuses = []

    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        if instance.id != "i-006b53dce5fb1d1c6":
            ec2list.append(instance.id)
            statuses.append(instance.state['Name'])
            
    print(ec2list)
    print(statuses)
    ec2.instances.filter(InstanceIds = ec2list).terminate()

    
# list_ec2_instances()
# name_ec2_instance()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('-a', type=str, dest='accesskey', required=True, help='enter aws access key')
    # parser.add_argument('-s', type=str, dest='secretkey', required=True, help='enter aws secret key')
    parser.add_argument('-k', type=str, dest='keypair', required=True, help='enter filepath to ec2 keypair')
    args = parser.parse_args()
    # configure_aws(args.accesskey, args.secretkey)
    
    
    # SECURITY_GROUP_NAME = "ProductionSystem"
    # create_security_group(SECURITY_GROUP_NAME)
    # ec2_instances = {}
    # ec2_public_dns = {}
    # create_ec2_instances(SECURITY_GROUP_NAME)
    # write_to_file(ec2_public_dns)
    # print(ec2_public_dns)
    # print("wait for 20 seconds for instances to be ready")
    # time.sleep(20)
    # keypair_file = args.keypair
    # setup_ec2_instance("mysql", ec2_public_dns, keypair_file)
    # setup_ec2_instance("mongodb", ec2_public_dns, keypair_file)
    # setup_ec2_instance("backend", ec2_public_dns, keypair_file)
    # setup_ec2_instance("frontend", ec2_public_dns, keypair_file)

    terminate_ec2_instances()
#"/mnt/c/Users/AG/Desktop/test1.pem"