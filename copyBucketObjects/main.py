#!/usr/bin/env python3

import argparse
import csv

import boto3
import botocore.exceptions


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Tool used to copy S3 Objects from one Bucket to another'
    )
    parser.add_argument('-profile', type=str, default=None,
                        help='AWS Profile, if not provided take your environment configuration')
    parser.add_argument('-csv', type=str, required=True,
                        help='Local path to your CSV file containing details about the objects source and destination')
    parser.add_argument('-auto-approve', dest='auto_approve', action='store_true',
                        help='Skips all interactive approval when a key already exists in destination')
    parser.set_defaults(auto_approve=False)

    args = parser.parse_args()
    return args


def get_bucket_from_path(path):
    split_path = path.split('/', 1)
    bucket_name = split_path[0]
    bucket_path = ''
    if len(split_path) > 1:
        bucket_path = split_path[1]
    return bucket_name, bucket_path


def fmt_key(path, name):
    if path == '':
        return name
    return f'{path}/{name}'


def validate_scope(sentence):
    validation = input(sentence)
    if validation == 'y':
        return True
    else:
        return False


def verify_destination(args, s3, dest_bucket, dest_key):
    try:
        s3.Object(dest_bucket, dest_key).load()
        if not args.auto_approve and not validate_scope('Destination key already exists, are you sure you want to overwrite this object (y): '):
            print('Stop copying file.')
            return False
    except botocore.exceptions.ClientError as _:
        return True
    return True


def copy(args, name, src, dest):
    src_bucket, src_path = get_bucket_from_path(src)
    dest_bucket, dest_path = get_bucket_from_path(dest)
    src_key = fmt_key(src_path, name)
    dest_key = fmt_key(dest_path, name)
    s3 = args.aws_session.resource('s3')
    print(f'\nCopying {name}...')
    if not verify_destination(args, s3, dest_bucket, dest_key):
        return
    try:
        bucket = s3.Bucket(dest_bucket)
        bucket.copy({
            'Bucket': src_bucket,
            'Key': src_key,
        }, dest_key)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(f'{src_bucket} does not exist or doesn\'t have {src_key} object: \n', e)
        elif e.response['Error']['Code'] == 'NoSuchBucket':
            print(f'{dest_bucket} not found: \n', e)
        else:
            print(f'error while copying {name}: \n', e)
        return
    print(f'{src_key} from {src_bucket} has been copied to {dest_bucket} in {dest_key}.')


def copy_objects():
    args = parse_arguments()

    if args.profile is not None:
        args.aws_session = boto3.session.Session(profile_name=args.profile)
    else:
        args.aws_session = boto3.session.Session()

    with open(args.csv, newline='') as csvfile:
        print(f'Reading {args.csv}...')
        reader = csv.DictReader(csvfile)
        for row in reader:
            copy(args, row['name'], row['source_path'], row['destination_path'])


if __name__ == '__main__':
    copy_objects()
