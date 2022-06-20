#!/usr/bin/env python3

import argparse

import boto3
import botocore.exceptions


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Tool used to delete empty and non-empty S3 Buckets'
    )
    parser.add_argument('-names', nargs='+', default=[], required=True,
                        help='List of S3 Bucket names')
    parser.add_argument('-profile', type=str, default=None,
                        help='AWS Profile, if not provided take your environment configuration')
    parser.add_argument('-auto-approve', dest='auto_approve', action='store_true',
                        help='Skips interactive approval of S3 Buckets & S3 Bucket files deletion')
    parser.set_defaults(auto_approve=False)

    args = parser.parse_args()
    return args


# Delete all files in a S3 Bucket
def cleanup_s3_bucket(s3_bucket):
    # Delete S3 objects
    for s3_object in s3_bucket.objects.all():
        s3_object.delete()
    # Delete S3 Object Versioning
    for s3_object_ver in s3_bucket.object_versions.all():
        s3_object_ver.delete()


def validate_scope(sentence):
    validation = input(sentence)
    if validation == 'y':
        return True
    else:
        return False


def delete_buckets():
    args = parse_arguments()

    print('Buckets to delete: ', args.names)
    if not args.auto_approve and not validate_scope('Are you sure you want to delete those buckets (y): '):
        return

    if args.profile is not None:
        aws_session = boto3.session.Session(profile_name=args.profile)
    else:
        aws_session = boto3.session.Session()

    client = aws_session.client('s3')
    for name in args.names:
        print(f'\nDeleting {name}...')
        try:
            client.delete_bucket(Bucket=name)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'BucketNotEmpty':
                print(f'{name} is not empty.')
                if args.auto_approve or\
                        validate_scope('Are you sure you want to delete all files in this bucket (y): '):
                    resource = aws_session.resource("s3")
                    s3_bucket = resource.Bucket(name)
                    cleanup_s3_bucket(s3_bucket)
                    client.delete_bucket(Bucket=name)
                else:
                    continue
            elif e.response['Error']['Code'] == 'NoSuchBucket':
                print(f'{name} doesn\'t exist:\n', e)
                continue
            else:
                print(f'error while deleting {name}:\n', e)
                continue
        print(f'{name} has been deleted.')


if __name__ == '__main__':
    delete_buckets()
