example-meta-review-dump
========================

Demonstrates how to download a flat file containing meta-reviews of all hotels in TrustYou's database from the "trustyou-api" Amazon S3 bucket, and how to process the downloaded JSON data.

Installation
------------

The Python example (download_meta_review_dump.py) runs with Python 2 or 3. It uses the [boto3 library](https://aws.amazon.com/sdk-for-python/). The example written in Bash (download_meta_review_dump.sh) needs the [AWS Command Line Interface](http://aws.amazon.com/cli/). Both can be installed by running:

```
pip install -r requirements.txt
```

Example
-------

Note that you need to contact TrustYou to receive your AWS access keys and secret keys before running these.

Download the latest meta-review dump into a folder called "meta-review-dump":

Run this once to confiture your AWS access key and secret:
```
aws configure
```

Then, to download and process the latest files:
```
./download_meta_review_dump.py meta-review-dump
./process_meta_review_dump.py meta-review-dump/TIMESTAMP_OF_DOWNLOADED_DUMP
```

For downloading hotel dump
```
./hotel_dump.py hotel-dump
```
