# aws-snapshotalyzer
Automation project for AWS

## About

This project uses boto3 to automate the AWS operation and snapshots


## Configuration

This program uses 'snapshotty' profile to handle the connectivity with AWS CLI

`aws configure --profile snapshotty`


## Running

`pipenv run "python snapshotty/snapshotty.py <command> <subcommand> <--project=PROJECT>"`

*command* instances, volumes, snapshots

*subcommand*

list for all the commands

start, stop, reboot for instances

create for snapshots

*project* is optional for all the commands

*instance* is optional for all the commands

*age* is optional for snapshots

*--force* is to start, stop and create snapshots all the instances
