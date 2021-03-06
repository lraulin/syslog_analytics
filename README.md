# syslog_analytics

## Purpose

Process csv files in the format:

### Input

<table class="table table-bordered table-hover table-condensed">
<thead><tr><th title="Field #1">Time</th>
<th title="Field #2">Event Type</th>
<th title="Field #3">Sensor</th>
<th title="Field #4">Message</th>
</tr></thead>
<tbody><tr>
<td>Apr 4, 2019 14:10:20 UTC</td>
<td>dns</td>
<td>syslog.idn.dot.gov-network</td>
<td>&lt;174&gt;Apr  4 14:10:20 152.120.3.200 named[21871]: 04-Apr-2019 10:10:20.760 queries: info: client 152.120.120.143#55623 (www.cybrary.it): query: www.cybrary.it IN A + (152.120.3.200)</td>
</tr>
</tbody></table>

### Output

<table class="table table-bordered table-hover table-condensed">
<thead><tr><th title="Field #1">DATE</th>
<th title="Field #2">TIME</th>
<th title="Field #3">IP ADDRESS OF THE CLIENT</th>
<th title="Field #4">QUERY DOMAIN</th>
<th title="Field #5">MESSAGE</th>
</tr></thead>
<tbody><tr>
<td>04/04/2019</td>
<td>14:10:20 UTC</td>
<td>152.120.120.143</td>
<td>www.cybrary.it</td>
<td>&lt;174&gt;Apr  4 14:10:20 152.120.3.200 named[21871]: 04-Apr-2019 10:10:20.760 queries: info: client 152.120.120.143#55623 (www.cybrary.it): query: www.cybrary.it IN A + (152.120.3.200)</td>
</tr>
</tbody></table>

## Installation

    python3 -m pip install -U dateparser
    python3 -m pip install -U --no-deps --index-url https://test.pypi.org/simple/ syslog_analytics

Assumes [Python 3](https://www.python.org/downloads/) and [Pip for Python 3](https://docs.python.org/3/installing/index.html) (usually installed automatically with Python) are installed. (The 'dateparser' dependency needs to be installed manually, because I published to the 'test' repository instead of the main one, and pip apparently has trouble using different sources at the same time.)

## Usage

    usage: syslog_analytics [-h] [-v] [files [files ...]]

    Process one or more csv files. Save results to output.csv in the current
    directory.

    positional arguments:
      files          one or more csv files to process

    optional arguments:
      -h, --help     show this help message and exit
      -v, --version  display version number

### Example

    syslog_analytics *.csv

Arguments will be treated as a list of csv files to be processed. The results from all files will be combined into a single output file, sorted by date/time.

## Assumptions

Input files are csv files as shown above. Files contain a header. The first column contains a date/time (any standard format should be ok). The fourth column contains the message to be parsed. Messages contain an IP proceeded by the string "client " and followed by "#" and a domain name between "query: " and "IN". Deviation from these assumptions may produce unexpected results.
