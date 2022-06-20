# 🗑 Delete S3 Buckets

As its name implies, *deleteBuckets* allows you to delete a given list of S3 Buckets whether they are empty or not.

## Dependencies

- [Python >= 3](https://www.python.org/downloads/)

## Installation

```commandline
pip install -r requirements.txt
```

## 🚀 Usage

```shell
$ ./main.py --help
usage: main.py [-h] -names NAMES [NAMES ...] [-profile PROFILE] [-auto-approve]

Tool used to delete empty and non-empty S3 Buckets

optional arguments:
  -h, --help            show this help message and exit
  -names NAMES [NAMES ...]
                        List of S3 Bucket names
  -profile PROFILE      AWS Profile, if not provided take your environment configuration
  -auto-approve         Skips interactive approval of S3 Buckets & S3 Bucket files deletion
```

- `-names` - List of S3 Bucket Names.
- `-profile` - The AWS Profile you want to use to execute the deletion. If none is provided it will use your environment variables such as AWS credentials or `AWS_PROFILE`.
- `-auto-approve` - Skips interactive approval of S3 Buckets and S3 Bucket files deletion. By default, *deleteBuckets* will always ask you before deleting all the Bucket and before deleting files in a non-empty Bucket.

### ✨ Examples

#### Delete Multiple S3 Buckets using AWS Profile

```shell
$ ./main.py -names bucket-delete-script-1 bucket-delete-script-2 -profile my-aws-profile
```

#### Delete One S3 Bucket
```shell
$ ./main.py -names bucket-delete-script-1
```
