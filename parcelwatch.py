#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from notifications.sms import ComtubeRuSMS


def parse_args():
    parser = OptionParser()

    parser.add_option("", "--user", action="store",
        dest="user", help="comtube's service user name")
    parser.add_option("", "--password", action="store",
        dest="password", help="password")
    parser.add_option("", "--mobile", action="store",
        dest="mobile", help="number of mobile phone to send sms to")
    parser.add_option("", "--message", action="store",
        dest="message", help="message to send (in UTF-8)")

    opts, args = parser.parse_args()

    if not (opts.user and opts.password and opts.mobile and opts.message):
        parser.error("Not enough args. given. Try --help switch for details.")

    return opts


def main():
    opts = parse_args()

    sender = ComtubeRuSMS(opts.user, opts.password, opts.mobile)
    (code, status) = sender.send(opts.message)
    print "%i\n%s" % (code, status)


if __name__ == '__main__':
    main()