#!/usr/bin/env bash

usage() {
cat << EOF
Usage:
	$0 [dest_folder]
	$0 -h

Download the latest full meta-review dump into the destination folder provided as the first argument.

Assumes that you have installed awscli (http://aws.amazon.com/cli/) and run "aws configure" to set up your access key and secret key.
EOF
}

if [[ $# -ne 1 || "$1" = "-h" ]]; then
    usage
    exit 1
fi

dest_folder="$1"

info() { cat <<< "$@" 1>&2; }

info "Determining latest date"

# from all the "done" files we find in the bucket ...
done_files=$(aws --profile test-user s3 ls s3://trustyou-api/meta-review/ --recursive | grep done$)
# ... pick the latest one, i.e. the last one in lexographical order
latest_date=$(grep -E -o "meta-review/[^/]+" <<< "$done_files" | tail -1)

# create local download dir, if necessary
mkdir -p $dest_folder/$latest_date/

info "Downloading meta-review dump"

# we use the convenient "sync" command, which will automatically resume an interrupted download
aws --profile test-user s3 sync s3://trustyou-api/$latest_date/ $dest_folder/$latest_date/ --exclude done
