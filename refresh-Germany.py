#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" refresh-germany.py: A script retrieving the german holidays for taskwarrior

Usage:
    refresh-germany.py [--state <German State abbreviated>]
    refresh-germany.py (-h | --help)

Options:
    -h, --help      Show this help
    --state <state> The two letter abbreviation for the German states
                    BW: Baden-Württemberg
                    BY: Bayern
                    BE: Berlin
                    BB: Brandenburg
                    HB: Bremen
                    HH: Hamburg
                    HE: Hessen
                    MV: Mecklenburg-Vorpommern
                    NI: Niedersachsen
                    NW: Nordrhein-Westfalen
                    RP: Rheinland-Pfalz
                    SL: Saarland
                    SN: Sachsen
                    ST: Sleswig-Holstein
                    SH: Sachen-Anhalt
                    TH: Thüringen
"""

import os
import json
import datetime
import time
import urllib.request

from docopt import docopt


class GermanHoliday(object):
    def __init__(self, state_abbr=None):
        self.api_url = self.get_holiday_url(state_abbr)
        self.holidays = self.get_holidays()

    @staticmethod
    def get_holiday_url(state_abbr, year=2017):
        """
        Compile the URL to retrieve the dates from
        :param state_abbr: Abbreviation of the German state to retrieve the holidays for
        :type state_abbr: str
        :param year: Year for which to retrieve the holiday dates
        :type year: int
        :return: URL to retrieve the dates from
        :rtype: str
        """
        german_states = [
            "BW", "BY", "BE", "BB",
            "HB", "HH", "HE", "MV",
            "NI", "NW", "RP", "SL",
            "SN", "ST", "SH", "TH"
        ]

        if state_abbr in german_states:
            state_abbr = state_abbr.upper()
        else:
            state_abbr = ','.join(german_states)

        api_url = 'https://ipty.de/feiertag/api.php'\
                  + '?do=getFeiertage' \
                  + '&loc=' + state_abbr\
                  + '&outformat=Y_m_d'\
                  + '&jahr='+str(year)

        return api_url

    def get_holidays(self):
        """
        Retrieve the dates and convert them to a dictionary
        :return: The holidays in dictionary form
        :rtype: dict
        """
        holidays_site = urllib.request.urlopen(self.api_url)
        holidays_json = holidays_site.read().decode()
        holidays_dict = json.loads(holidays_json)

        return holidays_dict

if __name__ == "__main__":
    arguments = docopt(__doc__, version="Refresh holidays germany 1.0")
    state = arguments['--state']

    holidays = GermanHoliday(state)
    print(holidays.api_url)
    print(holidays.get_holidays())
