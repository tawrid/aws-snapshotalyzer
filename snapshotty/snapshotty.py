import boto3
import click

session = boto3.Session(profile_name='snapshotty')
ec2 = session.resource('ec2')

@click.command()
def list_instances():
    for i in ec2.instances.all():
        print("ID: {0}".format(i.id))
        print("Instance Type: {0}".format(i.placement['AvailabilityZone']))
        print("Placement: {0}".format(i.id))
        print("State: {0}".format(i.state['Name']))
        print("Public DNS Name: {0}".format(i.public_dns_name))
        print("Public IP Address: {0}".format(i.public_ip_address))
        print("Security Groups: {0}".format(str(i.security_groups)))
        print("--------------------------")
    return

if __name__ == '__main__':
    list_instances()
