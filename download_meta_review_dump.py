#!/usr/bin/env python
"""
Demonstration of how to download a complete meta-review API dump.
"""

from getpass import getpass
import logging
import os.path
import re
import sys

import boto

def parse_args():
	from argparse import ArgumentParser
	argp = ArgumentParser(__doc__)
	argp.add_argument("--dest_folder", help="Existing empty folder where files should be stored", required=True)
	return argp.parse_args()

def download_latest(aws_access_key, aws_secret_key, dest_folder):
	
	logging.info("Connecting to Amazon S3")

	# Connect to Amazon S3 using credentials.
	conn = boto.connect_s3(aws_access_key, aws_secret_key)

	# Select the bucket containing dumps of the TrustYou API.
	bucket = conn.get_bucket("trustyou-api-us-staging")

	# The trustyou-api-us-staging bucket contains snapshots of the TrustYou API at
	# different points in time. They are organized in folders whose name is
	# a timestamp.

	logging.info("Looking for latest complete dump")
	
	latest_date = None
	for key in bucket.list(prefix="meta-review/"):
		done_file_match = re.match("^meta-review/([^/]+)/done$", key.key)
		if done_file_match:
			date = done_file_match.group(1)
			latest_date = max(date, latest_date)

	assert latest_date is not None, "No complete dump folder found!"

	logging.info("Downloading dump from %s", latest_date)

	target_folder = os.path.join(dest_folder, "meta-review", latest_date)
	if not os.path.exists(target_folder):
		os.makedirs(target_folder)

	for key in bucket.list(prefix="meta-review/{}/".format(latest_date)):
		basename = key.key.split("/")[-1]
		if basename == "done":
			continue
		local_path = os.path.join(target_folder, basename)
		if os.path.exists(local_path):
			logging.debug("- Skipping %s, already downloaded", local_path)
			continue
		logging.debug("- Downloading %s", key.key)
		local_tmp_path = local_path + "_tmp"
		key.get_contents_to_filename(local_tmp_path)
		os.rename(local_tmp_path, local_path)

if __name__ == "__main__":

	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
	logging.getLogger("boto").setLevel(logging.INFO)
	
	args = parse_args()
	
	logging.info("Download latest meta-review dump to %s", args.dest_folder)

	assert os.path.exists(args.dest_folder) and os.path.isdir(args.dest_folder), "Output folder does not exist!"

	aws_access_key = getpass("Please enter your AWS access key and press Enter (characters not visible): ")
	aws_secret_key = getpass("AWS secret key: ")

	download_latest(aws_access_key, aws_secret_key, args.dest_folder)

	logging.info("Done!")
