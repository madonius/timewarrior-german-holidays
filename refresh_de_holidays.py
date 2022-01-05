#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" refresh-germany.py: A script retrieving the german holidays for taskwarrior

Usage:
    refresh-germany.py [--state <German State abbreviated> --year <year>]
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
    --year <year>   The year for which data shall be returned
"""

import json
from datetime import datetime
import urllib.request

from docopt import docopt


class GermanHoliday(object):
    """ Retrieves the German holidys and preformats them for timewarrior """
    def __init__(self, state_abbr=None, year=None):
        """
        :param state_abbr: The abbreviation for the state
        :type state_abbr: str
        """
        if not year:
            year = datetime.now().year
        self.api_url = self.get_holiday_url(state_abbr, year)
        self.holidays = self.get_holidays()
        self.header = self.get_header()

    @staticmethod
    def get_holiday_url(state_abbr, year):
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
                  + '&outformat=Y-m-d'\
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

    def get_header(self):
        """
        Header for the timewarrior holiday file
        :return: Timewarrior hiliday file header
        :rtype: str
        """

        api_url = self.api_url

        header = "# Holiday data provided by ipty.de\n"\
                 +"#\t%s\n" % api_url\
                 +"#\tGenerated %s\n" % datetime.strftime(datetime.today(), "%c")\
                 +"\n"\
                 +"define holidays:\n"\
                 +"  de-DE:\n"

        return header

    def format_output(self):
        """
        Generate formatted output in the timewarrior holiday format
        :return: Timewarrior holidays for Germany
        :rtype: str
        """
        holidays = self.holidays
        header = self.get_header()
        formated_holidays = ""

        for holiday in holidays:
            holiday_format = "    %s = %s\n" % (holiday['date'].replace('-','_'), holiday['title'])
            formated_holidays += holiday_format

        return header+formated_holidays


def main():
    """ Create the output
    :return: None
    :rtype: null
    """
    arguments = docopt(__doc__, version="Refresh holidays germany 1.0")
    state = arguments['--state']
    year = arguments['--year']

    de_holidays = GermanHoliday(state, year)
    print(de_holidays.format_output())


if __name__ == "__main__":
    main()
