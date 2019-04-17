import argparse
import csv
import dateparser
import datetime
import pkg_resources
import re
from itertools import chain
from operator import itemgetter

DATE_FORMAT = "%m/%d/%Y"  # 04/16/2016
TIME_FORMAT = "%H:%M:%S %Z"  # 20:36:05.
CLIENT_IP_PATTERN = re.compile(
    r'client\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})#\d+')
QUERY_DOMAIN_PATTERN = re.compile(r'query:\s+(\S+)\s+IN')
HEADERS = ["DATE", "TIME", "IP ADDRESS OF THE CLIENT",
           "QUERY DOMAIN", "MESSAGE"]


def get_rows(csv_file):
    with open(csv_file, newline='') as f:
        rows = [row for row in csv.reader(f)]
    return rows[1:]


def transform_row(row):
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
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='files', type=str,
                        nargs='*', help='One or more csv files to process'),
    parser.add_argument('-v', '--version', action='store_true',
                        dest='version', help='Display version number')
    args = parser.parse_args()

    if not any(vars(args).values()):
        print('No arguments provided.')
        parser.print_help()

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
        writer = csv.writer(f)
        writer.writerows(new_rows)


if (__name__ == "__main__"):
    main()
