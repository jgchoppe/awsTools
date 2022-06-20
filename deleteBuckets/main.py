#!/usr/bin/env python3
import argparse
from re import A
import boto3
import botocore.exceptions


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Tool used to delete S3 Buckets'
    )
    parser.add_argument('-n', '--names', nargs='+', default=[])
    parser.add_argument('--profile', type=str, default='',
                        help='AWS Profile, if not provided take your environment configuration')

    args = parser.parse_args()
    return args


def cleanup_s3_bucket(s3_bucket):
    # Delete S3 objects
    for s3_object in s3_bucket.objects.all():
        s3_object.delete()
    # Delete S3 Object Versioning
    for s3_object_ver in s3_bucket.object_versions.all():
        s3_object_ver.delete()


def validate_scope(sentence):
    validation = input(sentence)
    if validation == "y":
        return True
    else:
        return False


def delete_buckets():
    args = parse_arguments()

    print("Buckets to delete: ", args.names)
    if not validate_scope("Are you sure you want those buckets (y): "):
        return

    aws_session = None
    if args.profile != "":
        aws_session = boto3.session.Session(profile_name=args.profile)
    else:
        aws_session = boto3.session.Session()

    client = aws_session.client("s3")
    for name in args.names:
        print(f'Deleting {name}...')
        try:
            client.delete_bucket(Bucket=name)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'BucketNotEmpty':
                print(f'{name} is not empty.')
                if validate_scope("Are you sure you want to delete all files in this bucket (y): "):
                    resource = aws_session.resource("s3")
                    s3_bucket = resource.Bucket(name)
                    cleanup_s3_bucket(s3_bucket)
                    client.delete_bucket(Bucket=name)
            else:
                print(e)
        print(f'${name} has been deleted')


if __name__ == '__main__':
    delete_buckets()
