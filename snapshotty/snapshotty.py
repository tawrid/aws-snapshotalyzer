import boto3
import click

session = boto3.Session(profile_name='snapshotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []
    if project:
        filters = [{'Name': 'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances

@click.group()
def instances():
    """Commands for instances"""

@instances.command("list")
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 Instances"
    instances = filter_instances(project)

    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        print("ID: {0}".format(i.id))
        print("Instance Type: {0}".format(i.placement['AvailabilityZone']))
        print("Placement: {0}".format(i.id))
        print("State: {0}".format(i.state['Name']))
        print("Public DNS Name: {0}".format(i.public_dns_name))
        print("Public IP Address: {0}".format(i.public_ip_address))
        print("Security Groups: {0}".format(str(i.security_groups)))
        print("Tags: {0}".format(tags.get("Project", "<No Project>")))
        print("--------------------------")
    return

@instances.command("stop")
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 Instances"
    instances = filter_instances(project)

    for i in instances:
        try:
            i.stop()
            print("Stopping instance {0}......".format(i.id))
        except:
            print("Instance {0} cannot be stopped at the moment".format(i.id))

@instances.command("start")
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def start_instances(project):
    "Start EC2 Instances"
    instances = filter_instances(project)

    for i in instances:
        try:
            i.start()
            print("Starting instance {0}.......".format(i.id))
        except:
            print("Instance {0} cannot be started at the moment".format(i.id))

if __name__ == '__main__':
    instances()
