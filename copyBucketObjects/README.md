# 📂 Copy S3 Bucket Objects

As its name implies, *copyBucketObjects* allows you to copy objects from a S3 Bucket to another thanks to a **CSV** file.

## Dependencies

- [Python >= 3](https://www.python.org/downloads/)

## Installation

```commandline
pip install -r requirements.txt
```

## 🚀 Usage

```shell
$ ./main.py --help
usage: main.py [-h] [-profile PROFILE] -csv CSV [-auto-approve]

Tool used to copy S3 Objects from one Bucket to another

optional arguments:
  -h, --help        show this help message and exit
  -profile PROFILE  AWS Profile, if not provided take your environment configuration
  -csv CSV          Local path to your CSV file containing details about the objects source and destination
  -auto-approve     Skips all interactive approval when a key already exists in destination
```

- `-csv` - The path to your CSV file
- `-profile` - The AWS Profile you want to use to execute the deletion. If none is provided it will use your environment variables such as AWS credentials or `AWS_PROFILE`.
- `-auto-approve` - Skips interactive approval of S3 Buckets and S3 Bucket files deletion. By default, *deleteBuckets* will always ask you before deleting all the Bucket and before deleting files in a non-empty Bucket.

The CSV file contains the following row ([example](example.csv)):
- `name` - The name of the file to copy, *e.g.:* `my_image.png`.
- `source_path` - The source path containing S3 Bucket name and path to the file, *e.g.:* `my-source-bucket-name/path/to/file`.
- `destination_path` - Same as above, but for the destination, *e.g.:* `my-destination-bucket-name/wherever/I/want`.

> Note that the Bucket for the source and the destination can be the same.

### ✨ Examples

#### Example without auto-approval

```shell
$ ./main.py -csv example.csv
Reading example.csv...

Copying my_file.png...
Destination key already exists, are you sure you want to overwrite this object (y): y
my_file.png from bucket-source-jg has been copied to bucket-destination-jg in path/to/dest/my_file.png.
```

#### Example with auto-approval

```shell
$ ./main.py -csv example.csv -auto-approval
Reading example.csv...

Copying my_file.png...
my_file.png from bucket-source-jg has been copied to bucket-destination-jg in path/to/dest/my_file.png.
```
