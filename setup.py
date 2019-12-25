from setuptools import setup

setup(
    name="aws-snapshotalizer",
    version="0.1",
    author="Tawrid Hyder",
    author_email="tawridnz@hotmail.com",
    summary="aws-snapshotalizer is a tool to manage the AWS instances and snapshots",
    license="GPLv3+",
    packages=['snapshotty'],
    url="https://github.com/tawrid/aws-snapshotalyzer",
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        snapshotty=snapshotty.snapshotty:cli
        ''',
)
