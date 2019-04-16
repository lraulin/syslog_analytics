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
<thead><tr><th title="Field #1">Time</th>
<th title="Field #2">Event Type</th>
<th title="Field #3">Sensor</th>
<th title="Field #4">Message</th>
</tr></thead>
<tbody><tr>
<td>Apr 4, 2019 14:00:28 UTC</td>
<td>dns</td>
<td>syslog.idn.dot.gov-network</td>
<td>&lt;174&gt;Apr  4 14:00:28 152.120.4.100 named[7604]: 04-Apr-2019 10:00:28.461 queries: info: client 152.120.186.45#54250 (sstats.arstechnica.com): query: sstats.arstechnica.com IN A + (152.120.4.100)</td>
</tr>
</tbody></table>

## Installation

    python3 -m pip install -U --index-url https://test.pypi.org/simple/ --no-deps syslog_analytics

## Usage

    syslog_analytics *.csv

Arguments will be treated as a list of csv files to be processed. The results from all files will be combined into a single output file.
