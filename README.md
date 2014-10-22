example-meta-review-dump
========================

Demonstrates how to download a flat file containing meta-reviews of all hotels in TrustYou's database from the "trustyou-api" Amazon S3 bucket.

Installation
------------

The Python example (download_meta_review_dump.py) runs with Python 2 or 3. It uses the [boto library](https://boto.readthedocs.org/en/latest/). The example written in Bash (download_meta_review_dump.sh) needs the [AWS Command Line Interface](http://aws.amazon.com/cli/). Both can be installed by running:

```
pip install -r requirements.txt
```

Example
-------

Note that you need to contact TrustYou to receive your AWS access keys and secret keys before running these.

Download the latest meta-review dump into a folder called "meta-review-dump":

```
aws configure # needs to be run only once
./download_meta_review_dump.sh meta-review-dump
```

```
./download_meta_review_dump.py --dest_folder meta-review-dump
```
