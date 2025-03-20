"""
Shadowserver Reports API Collector Bot

SPDX-FileCopyrightText: 2020 Intelmq Team <intelmq-team@cert.at>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
from datetime import datetime, timedelta, timezone
import json
import hashlib
import hmac
import re
from typing import Optional

import requests.exceptions

from intelmq.lib.bot import CollectorBot
from intelmq.lib.mixins import HttpMixin, CacheMixin


APIROOT = 'https://transform.shadowserver.org/api2/'
DLROOT  = 'https://dl.shadowserver.org/'
FILENAME_PATTERN = re.compile(r'\.csv$')


class ShadowServerAPICollectorBot(CollectorBot, HttpMixin, CacheMixin):
    """
    Connects to the Shadowserver API, requests a list of all the reports for an organization and processes the ones that are new

    Parameters:
        api_key (str): Your Shadowserver API key
        secret (str): Your Shadowserver API secret
        country (str): DEPRECATED The mailing list you want to download reports for (i.e. 'austria')
        reports (list):
            A list of strings or a comma-separated list of the mailing lists you want to process.
        types (list):
            A list of strings or a string of comma-separated values with the names of report types you want to process. If you leave this empty, all the available reports will be downloaded and processed (i.e. 'scan', 'drones', 'intel', 'sandbox_connection', 'sinkhole_combined').
    """

    country = None
    api_key = None
    secret = None
    types = None
    reports = None
    rate_limit: int = 86400
    redis_cache_db: int = 12
    redis_cache_host: str = "127.0.0.1"  # TODO: type could be ipadress
    redis_cache_port: int = 6379
    redis_cache_ttl: int = 864000  # 10 days
    redis_cache_password: Optional[str] = None
    _report_list = []
    _type_list = []

    def init(self):
        if not self.api_key:
            raise ValueError('No api_key provided.')
        if not self.secret:
            raise ValueError('No secret provided.')

        if isinstance(self.reports, str):
            # if reports is an empty string (or only contains whitespace), behave as if the parameter is not set and select all reports
            reports = self.reports.strip()
            self._report_list = reports.split(',') if reports else []
        elif isinstance(self.reports, list):
            self._report_list = self.reports
        if isinstance(self.types, str):
            # if types is an empty string (or only contains whitespace), behave as if the parameter is not set and select all types
            types = self.types.strip()
            self._type_list = types.split(',') if types else []
        elif isinstance(self.types, list):
            self._type_list = self.types
        if self.country and self.country not in self._report_list:
            self.logger.warn("Deprecated parameter 'country' found. Please use 'reports' instead. The backwards-compatibility will be removed in IntelMQ version 4.0.0.")
            self._report_list.append(self.country)

        self.preamble = f'{{ "apikey": "{self.api_key}" '

    def check(parameters: dict):
        for key in parameters:
            if key == 'file_format':
                return [["error", "The file_format parameter is no longer supported. All reports are CSV."]]
            elif key == 'country':
                return [["warning", "Deprecated parameter 'country' found. Please use 'reports' instead. The backwards-compatibility will be removed in IntelMQ version 4.0.0."]]

    def _headers(self, data):
        return {'HMAC2': hmac.new(self.secret.encode(), data.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()}

    def _reports_list(self, date=None):
        """
        Get a list of all the reports shadowserver has for an organization
        via the reports/list endpoint. If a list of types is set in the
        parameters, we only process reports with those types.
        To be on the safe side regarding different calculations of timestamps,
        we request reports over a timespan of four days: two days in the past
        until one day in the future.
        The names of processed reports are cached and therefore not processed
        again.
        """
        if date is None:
            date = datetime.now(timezone.utc).date()
        begin = date - timedelta(2)

        data = self.preamble
        data += f',"date": "{begin.isoformat()}:{date.isoformat()}" '
        if len(self._report_list) > 0:
            data += f',"reports": {json.dumps(self._report_list)}'
        data += '}'
        self.logger.debug('Downloading report list with data: %s.', data)

        response = self.http_session().post(APIROOT + 'reports/list', data=data, headers=self._headers(data))
        response.raise_for_status()

        reports = response.json()
        self.logger.debug('Downloaded report list, %s entries.', len(reports))

        if 'error' in reports:
            self.logger.debug('There was an error downloading the reports: %s', reports['error'])
            return None

        if self._type_list:
            reports = [report for report in reports if any(report['type'] == rtype for rtype in self._type_list)]
        return reports

    def _report_download(self, reportid: str):
        """
        Download one report from the shadowserver API via the reports/download endpoint
        """
        data = self.preamble
        data += f',"id": "{reportid}"}}'
        self.logger.debug('Downloading report with data: %s.', data)
        response = self.http_session().get(DLROOT + reportid)
        response.raise_for_status()

        return response.text

    def process(self):
        """
        Download reports and send them.
        Cache the filename of the report to not download the same report again.
        """
        reportslist = self._reports_list()
        self.logger.debug('Reports list contains %s entries after filtering.', len(reportslist))

        reports_downloaded = 0

        for item in reportslist:
            filename = item['file']
            filename_fixed = FILENAME_PATTERN.sub('.csv', filename, count=1)
            if self.cache_get(filename):
                self.logger.debug('Processed file %r (fixed: %r) already.', filename, filename_fixed)
                continue
            self.logger.debug('Processing file %r (fixed: %r).', filename, filename_fixed)
            try:
                reportdata = self._report_download(item['id'])
                report = self.new_report()
                report.add('extra.file_name', filename_fixed)
                report.add('raw', reportdata)
                self.send_message(report)
                self.cache_set(filename, 1)
                self.logger.debug('Sent report: %r (fixed: %r, size: %.3g KiB).', filename, filename_fixed,
                                  len(reportdata) / 1024)  # TODO: Replace by a generic size-conversion function
                reports_downloaded += 1
            except requests.exceptions.ReadTimeout:
                self.logger.error("Timeout on data download: %r, %r!", item['file'], item['id'])
        self.logger.info('Downloaded %d of %d available reports.', reports_downloaded, len(reportslist))


BOT = ShadowServerAPICollectorBot
