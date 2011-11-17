#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import tempfile
import shutil
import pickle

from optparse import OptionParser

from notifications.sms import ComtubeRuSMS
from parsers.russianpost import RussianPostQuery
from parsers.russianpost import RussianPostTrackingEntry
from shell import run_shell

def parse_args():
    parser = OptionParser()

    parser.add_option("", "--shell", action="store_true",
        dest="shell", default=False,
        help="run parcelwatch's shell for admin tasks")
    parser.add_option("", "--data-file", action="store",
        dest="data_file", help="file to store state between checks",
        metavar="FILE")
    parser.add_option("", "--user", action="store",
        dest="user", help="comtube's service user name")
    parser.add_option("", "--password", action="store",
        dest="password", help="comtube's service user's password")
    parser.add_option("", "--mobile", action="store",
        dest="mobile", help="number of mobile phone to send sms to")

    opts, args = parser.parse_args()

    if opts.shell and opts.data_file:
        return opts
    elif not (opts.data_file and opts.user and opts.password and opts.mobile):
        parser.error("Not enough args. given. Try --help switch for details.")

    return opts


def save_cache(opts, cache):
    tmp_data_file = tempfile.NamedTemporaryFile(delete=False)
    pickle.dump(cache, tmp_data_file)
    shutil.move(tmp_data_file.name, opts.data_file)


def load_cache(opts):
    created = False

    if os.path.exists(opts.data_file):
        data_file = open(opts.data_file, "r")
        cache = pickle.load(data_file)
    else:
        cache = dict()
        created = True

    return (cache, created)


def main():
    opts = parse_args()
    cache, new_cache = load_cache(opts)

    if opts.shell:
        run_shell(cache)
        save_cache(opts, cache)
        return

    handle = RussianPostQuery()
    sms = ComtubeRuSMS(opts.user, opts.password, opts.mobile)

    for identifier in cache.iterkeys():
        events = handle.query(identifier.strip())
        events_count = len(events)

        if new_cache:
            cache[identifier] = events
        else:
            if cache.has_key(identifier):
                cached_events = cache[identifier]
                cached_events_count = len(cached_events)
                if events_count > 0 and events_count > cached_events_count:
                    new_events_count = events_count - cached_events_count
                    first = cached_events_count
                    last = cached_events_count + new_events_count
                    for idx in xrange(first, last):
                        event = events[idx]
                        cached_events.append(event)
                        msg = "Отправление %s: %s" % (identifier, str(event))
                        code, status = sms.send(msg)
            else:       
                cache[identifier] = events

    save_cache(opts, cache)
    

if __name__ == '__main__':
    main()