#!/usr/bin/env python
"""
Demonstration of how to extract data from a meta-review dump. Usage:

$ ./download_meta_review_dump.py DOWNLOAD_FOLDER
$ ./process_meta_review_dump.py DOWNLOAD_FOLDER/TIMESTAMP_OF_DOWNLOADED_DUMP

For demonstration purposes, this script prints a custom summary sentence for every hotel. Copy this script, and customize it with your own business logic!
"""

from glob import glob
import gzip
import json
import logging
import os.path
import sys


def parse_args():
    from argparse import ArgumentParser
    argp = ArgumentParser(__doc__)
    argp.add_argument("dest_folder", help="Existing folder where meta-review dump was previously downloaded")
    return argp.parse_args()


def process_meta_review(meta_review):
    """
    Do something with the meta-review JSON!

    This is where you would:
    1. Translate meta_review["ty_id"] to your own hotel ID, dropping any unmapped hotels
    2. Traverse the JSON structure to find the data you are interested in, documented at
    http://api.trustyou.com/hotels/documentation.html
    3. Store data in your own database, to run reports, or serve them to a live website

    Here, for demonstration purposes, we print a little custom summary sentence.
    """

    ty_id = meta_review["ty_id"]
    trust_score = meta_review.get("summary", {}).get("score")

    badges = meta_review.get("badge_list", [])

    def strip_markup(text):
        """
        Badge texts contain some formatting hints. Remove them for display on the terminal.
        """
        return (text
                .replace("<strong class=\"label\">", "")
                .replace("</strong>", "")
                .replace("<span class=\"hotel-type\">", "")
                .replace("</span>", "")
                .replace("<strong>", "")
        )

    badge_texts = list(
        strip_markup(badge["text"])
        for badge
        in badges[1:] # skip the overall badge, which is always in first place
    )

    sentence = "Hotel {ty_id} has a score of {trust_score}, and got awarded these badges: {badge_texts}".format(
        ty_id=ty_id,
        trust_score=trust_score,
        badge_texts=(", ".join(badge_texts) or "No badges!")
    )

    print(sentence)


def process_meta_review_dump(dest_folder):
    """
    Look for all *.jsonl.gz files in the destination folder, and process each file line by line, calling
    process_meta_review on each JSON object.
    """

    logging.info("Processing meta-review dump at %s", args.dest_folder)

    # Find all *.jsonl.gz files in destination folder.

    pattern = os.path.join(dest_folder, "[0-9a-f][0-9a-f].jsonl.gz")
    gz_paths = glob(pattern)
    if len(gz_paths) < 256:
        logging.warning("Found less than 256 *.jsonl.gz files. Are you processing an incomplete meta-review dump?")

    # Process each zipped file.

    for gz_path in sorted(gz_paths):
        logging.debug("- Processing %s", gz_path)

        # Note that this is not the most performant way of unzipping files. In production, consider using "gunzip"
        # directly, and processing files in parallel, e.g. via "xargs":
        # $ find $dest_folder -name "*.jsonl.gz" | xargs -n1 -P16 gunzip

        with gzip.open(gz_path) as jsonl_file:
            for line_bytes in jsonl_file:

                # Load a single line from the *.jsonl file. Each line represents one meta-review. The same hotel will
                # appear on ~20 consecutive lines, once for every supported display language.

                # Identify the hotel with the "ty_id" property, and the language with "lang".

                line = line_bytes.decode("utf-8")
                meta_review = json.loads(line)

                # Here, for demonstration purposes, we will ignore all languages except English.

                if meta_review["lang"] != "en":
                    continue

                # Call your business logic on this meta-review!

                process_meta_review(meta_review)

if __name__ == "__main__":

    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    args = parse_args()

    assert os.path.exists(args.dest_folder) and os.path.isdir(args.dest_folder), "Destination folder does not exist!"

    process_meta_review_dump(args.dest_folder)

    logging.info("Done!")
