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
import urllib

from docopt import docopt


class GermanHoliday(object):
    def __init__(self, state_abbr=None):
        self.api_url = self.get_holiday_url(state_abbr)

    @staticmethod
    def get_holiday_url(state_abbr, year='2017'):
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
         + '?do=getFeiertage'\
         + '&loc=' + state_abbr\
         + '&outformat=Y-m-d'\
         + '&jahr='+str(year)

        return api_url

if __name__ == "__main__":
    arguments = docopt(__doc__, version="Refresh holidays germany 1.0")
    state = arguments['--state']

    holidays = GermanHoliday.get_holiday_url(state)
    print(holidays)