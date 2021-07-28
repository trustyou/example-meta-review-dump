Trustyou Meta-review and Hotel Dump Example
========================

Demonstrates how to download a flat file containing meta-reviews of all hotels in TrustYou's database from the "trustyou-api" Amazon S3 bucket, and how to process the downloaded JSON data.

# Installation

The Python example (download_meta_review_dump.py) runs with Python 2 or 3. It uses the [boto3 library](https://aws.amazon.com/sdk-for-python/). The example written in Bash (download_meta_review_dump.sh) needs the [AWS Command Line Interface](http://aws.amazon.com/cli/). Both can be installed by running:

```
pip install -r requirements.txt
```

> Note: you need to contact TrustYou to receive your AWS access key and secret key before running these.

Run this once to configure your AWS access key and secret:

```
aws configure
```

# Examples

## Download and process meta-review dump

Download the latest meta-review dump into a folder called `meta-review-dump`:

```
./download_meta_review_dump.py meta-review-dump
./process_meta_review_dump.py meta-review-dump/TIMESTAMP_OF_DOWNLOADED_DUMP
```

## Download hotel dump

Using s3 sync to download all hotel dumps into a folder called `hotel-dump`

```
aws s3 sync s3://trustyou-api/hotels/ hotel-dump
```
