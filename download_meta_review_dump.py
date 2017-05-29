#!/usr/bin/env python
"""
Demonstration of how to download a complete meta-review API dump.
"""

import hashlib
import logging
import os.path
import re
import sys

import boto3

def parse_args():
	from argparse import ArgumentParser
	argp = ArgumentParser(__doc__)
	argp.add_argument("dest_folder", help="Existing empty folder where files should be stored")
	return argp.parse_args()

def md5(path):
	"""
	Compute MD5 hash of file. Read it in chunks, so we don't need to fix the entire file in memory.
	"""
	hash_md5 = hashlib.md5()
	with open(path, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def download_latest(dest_folder):
	
	logging.info("Connecting to Amazon S3")

	# Connect to S3
	s3 = boto3.resource("s3")

	# Select the bucket containing dumps of the TrustYou API.
	bucket = s3.Bucket("trustyou-api")

	# The trustyou-api bucket contains snapshots of the TrustYou API at
	# different points in time. They are organized in folders whose name is
	# a timestamp.

	logging.info("Looking for latest complete dump")
	
	latest_date = None
	for object_summary in bucket.objects.filter(Prefix="meta-review/"):
		done_file_match = re.match("^meta-review/([^/]+)/done$", object_summary.key)
		if done_file_match:
			date = done_file_match.group(1)
			if latest_date is None or date > latest_date:
				latest_date = date

	assert latest_date is not None, "No complete dump folder found!"

	logging.info("Downloading dump from %s", latest_date)

	target_folder = os.path.join(dest_folder, "meta-review", latest_date)
	if not os.path.exists(target_folder):
		os.makedirs(target_folder)

	for object_summary in bucket.objects.filter(Prefix="meta-review/{}/".format(latest_date)):
		basename = object_summary.key.split("/")[-1]
		if basename == "done":
			continue
		local_path = os.path.join(target_folder, basename)
		if os.path.exists(local_path):
			logging.debug("- Skipping %s, already downloaded", object_summary.key)
			continue
		logging.debug("- Downloading %s", object_summary.key)
		local_tmp_path = local_path + "_tmp"
		object = object_summary.Object()
		object.download_file(local_tmp_path)
		expected_e_tag = '"{}"'.format(md5(local_tmp_path))  # E-Tag is returned with quotes around it by the API
		assert expected_e_tag == object.e_tag, "Checksums don't match, download failed!"
		os.rename(local_tmp_path, local_path)

if __name__ == "__main__":

	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
	logging.getLogger("botocore").setLevel(logging.CRITICAL)
	logging.getLogger("boto3").setLevel(logging.CRITICAL)
	logging.getLogger("s3transfer").setLevel(logging.CRITICAL)
	
	args = parse_args()
	
	logging.info("Download latest meta-review dump to %s", args.dest_folder)

	assert os.path.exists(args.dest_folder) and os.path.isdir(args.dest_folder), "Destination folder does not exist!"

	download_latest(args.dest_folder)

	logging.info("Done!")
