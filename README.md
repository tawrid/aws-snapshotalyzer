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
*subcommand* is list, start, stop
*project* is optional
