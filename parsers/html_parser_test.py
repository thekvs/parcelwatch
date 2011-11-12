#!/usr/bin/env python
# -*- coding: utf-8 -*-

from russianpost import RussianPostQuery, RussianPostParser
from russianpost import RussianPostTrackingEntry


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("", "--html", action="store",
        dest="html", help="html with tracking data", metavar="FILE")
    opts, args = parser.parse_args()

    if not opts.html:
        parser.error("Not enough args. given. Try --help switch for details.")

    data = open(opts.html, "r").read()

    rp_parser = RussianPostParser()
    resp = rp_parser.parse(data)

    for r in resp:
        print r
