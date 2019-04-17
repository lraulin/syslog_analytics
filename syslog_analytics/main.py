import argparse
import csv
import dateparser
import datetime
import pkg_resources
import re
from itertools import chain
from operator import itemgetter
from time import time

start_time = time()

DATE_FORMAT = "%m/%d/%Y"  # 04/16/2016
TIME_FORMAT = "%H:%M:%S %Z"  # 20:36:05.
CLIENT_IP_PATTERN = re.compile(
    r'client\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})#\d+')
QUERY_DOMAIN_PATTERN = re.compile(r'query:\s+(\S+)\s+IN')
HEADERS = ["DATE", "TIME", "IP ADDRESS OF THE CLIENT",
           "QUERY DOMAIN", "MESSAGE"]


def get_rows(csv_file):
    """Open csv file and return contents as list of lists."""
    with open(csv_file, newline='') as f:
        rows = [row for row in csv.reader(f)]
    return rows[1:]


def transform_row(row):
    """Process a row (list) in input format and return in output format."""

    row_data = {
        "EPOCH": None,
        "DATE": None,
        "TIME": None,
        "IP": None,
        "DOMAIN": None
    }

    dt = dateparser.parse(row[0])

    row_data["EPOCH"] = dt.timestamp()
    row_data["DATE"] = dt.strftime(DATE_FORMAT)
    row_data["TIME"] = dt.strftime(TIME_FORMAT)

    message = row[3]
    ip_match = CLIENT_IP_PATTERN.search(message)
    row_data["IP"] = ip_match.group(1) if ip_match else "!!! NO MATCH !!!"
    domain_match = QUERY_DOMAIN_PATTERN.search(message)
    row_data["DOMAIN"] = domain_match.group(
        1) if domain_match else "!!! NO MATCH !!!"

    new_row = [row_data["EPOCH"], row_data["DATE"], row_data["TIME"],
               row_data["IP"], row_data["DOMAIN"], message]
    return new_row


def main():
    # Set up command-line arguments with argparse.
    parser = argparse.ArgumentParser(
        description='Process one or more csv files. Save results to output.csv in the current directory.')
    parser.add_argument('files', metavar='files', type=str,
                        nargs='*', help='one or more csv files to process'),
    parser.add_argument('-v', '--version', action='store_true',
                        dest='version', help='display version number')
    args = parser.parse_args()

    # Print explaination and usage instructions if no arguments are provided.
    if not any(vars(args).values()):
        print('No arguments provided.')
        parser.print_help()
        exit()

    # Print version number if called with version flag.
    if args.version:
        version = pkg_resources.require('syslog_analytics')[0].version
        print(f'syslog_analytics v{version}')

    files = args.files

    rows = [row for row in chain.from_iterable(
        [get_rows(file) for file in files])]

    new_rows = [transform_row(row) for row in rows]
    new_rows = sorted(new_rows, key=itemgetter(0))
    new_rows = [HEADERS] + [row[1:] for row in new_rows]

    with open('output.csv', 'w', newline='') as f:
        print('Writing to output.csv...')
        writer = csv.writer(f)
        writer.writerows(new_rows)

    print(
        f"Finished processing {len(new_rows)-1} rows in {len(files)} files in {time()-start_time:.0f} seconds.")


if (__name__ == "__main__"):
    main()
