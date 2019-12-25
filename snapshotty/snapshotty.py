import boto3
import botocore
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

def has_pending_snapshot(volume):
    snapshots = list(volume.snapshots.all())
    return snapshots and snapshots[0].state == 'pending'

@click.group()
def cli():
    """Snapshot Management Program"""

@cli.group("snapshots")
def snapshots():
    """Commands for snapshots"""

@snapshots.command("list")
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
@click.option('--all', 'list_all', default=False, is_flag=True,
    help="List all the snapshots regardless old or new")
def list_snapshots(project, list_all):
    "List EC2 Snapshots"
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print("Instance ID: {0}".format(i.id))
                print("Volume ID: {0}".format(v.id))
                print("Snapshot ID: {0}".format(s.id))
                print("State: {0}".format(s.state))
                print("Progress: {0}".format(s.progress))
                print("Start Time: {0}".format(s.start_time.strftime("%c")))
                print("--------------------------")
                if s.state == 'completed' and not list_all:
                    break
    return

@snapshots.command("create")
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def create_snapshots(project):
    "Create EC2 Snapshots"
    instances = filter_instances(project)

    for i in instances:
        print("Instance {0} is stopping....".format(i.id))
        try:
            i.stop()
            i.wait_until_stopped()
            for v in i.volumes.all():
                print("Creating snapshots for volume {0}".format(v.id))
                if has_pending_snapshot:
                    print("Snapshot for volume {0} is already in progress. Skipping...".format(v.id))
                    continue
                v.create_snapshot(Description="Created by Snaphotty")
                print("Snapshot created for volume {0}".format(v.id))
                print("Instance {0} is starting....".format(i.id))
            i.start()
            i.wait_until_running()
        except botocore.exceptions.WaiterError as e:
            print("Error occured while creating snapshot for instance {0}".format(i.id) + str(e))
        print("Jobs Done.")
        print("--------------------------")
    return

@cli.group("volumes")
def volumes():
    """Commands for volumes"""

@volumes.command("list")
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 Volumes"
    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            # tags = {t['Key']: t['Value'] for t in i.tags or []}
            print("Instance ID: {0}".format(i.id))
            print("Volume ID: {0}".format(v.id))
            print("State: {0}".format(v.state))
            print("Size: {0} GiB".format(str(v.size)))
            print("Encrypted: {0}".format(v.encrypted and "Encrypted" or "Not Encrypted"))
            print("--------------------------")
    return

@cli.group("instances")
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
            print("Stopping instance {0}......".format(i.id))
            i.stop()
        except botocore.exceptions.ClientError as e:
            print("Instance {0} cannot be stopped at the moment. ".format(i.id) + str(e))
            continue

@instances.command("start")
@click.option('--project', default=None,
    help="Only instances for project (tag Project:<name>)")
def start_instances(project):
    "Start EC2 Instances"
    instances = filter_instances(project)

    for i in instances:
        try:
            print("Starting instance {0}.......".format(i.id))
            i.start()
        except botocore.exceptions.ClientError as e:
            print("Instance {0} cannot be started at the moment. ".format(i.id) + str(e))
            continue

if __name__ == '__main__':
    cli()
