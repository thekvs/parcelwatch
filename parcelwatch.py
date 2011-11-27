#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import tempfile
import shutil
import pickle
import logging
import traceback

from optparse import OptionParser
from ConfigParser import SafeConfigParser

from notifications.sms_notifier import ComtubeRuSMS
from notifications.email_notifier import Email

from parsers.russianpost import RussianPostQuery
from parsers.russianpost import RussianPostTrackingEntry

from shell import run_shell


def parse_args():
    parser = OptionParser()

    parser.add_option("", "--shell", action="store_true",
        dest="shell", default=False,
        help="run parcelwatch's shell for admin tasks")
    parser.add_option("", "--config", action="store",
        dest="config", help="configuration file",
        metavar="FILE")
    
    opts, args = parser.parse_args()

    if not opts.config:
        parser.error("Not enough args. given. Try --help for details.")

    return opts


def save_cache(conf, cache):
    data_file = conf.get("status", "file")
    tmp_data_file = tempfile.NamedTemporaryFile(delete=False)
    pickle.dump(cache, tmp_data_file)
    shutil.move(tmp_data_file.name, data_file)


def load_cache(conf):
    data_file = conf.get("status", "file")
    if os.path.exists(data_file):
        cache = pickle.load(open(data_file, "r"))
    else:
        cache = dict()

    return cache


def parse_config(config):
    conf = SafeConfigParser()
    conf.readfp(open(config))

    return conf


def init_logger(conf):
    logfile = conf.get("logging", "file")
    loglevel = logging.DEBUG

    logging.basicConfig(filename=logfile, level=loglevel,
        format="%(levelname)s|%(asctime)s|%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")


def send_notifications(sms, email, msg):
    try:
        sms_code, sms_status = sms.send(msg)
    except Exception as e:
        logging.error("Error while sending SMS "\
            "notification: %s", e)
    else:
        if sms_code == 200:
            logging.info("SMS notification sent: "\
                "code=%d, status=%s",
                sms_code, sms_status)
        else:
            logging.error("Error while sending SMS "\
                "notification: code=%d, status=%s",
                sms_code, sms_status)
        
    try:
        email.send(msg)
    except Exception as e:
        logging.error("Error while sending email "\
            "notification: %s", e)
    else:
        logging.info("Email notification sent")


def main(opts, conf):
    cache = load_cache(conf)

    if not opts.shell:
        handle = RussianPostQuery()

        sms_user = conf.get("sms", "comtube_user")
        sms_password = conf.get("sms", "comtube_password")
        mobile = conf.get("sms", "mobile")

        sms = ComtubeRuSMS(sms_user, sms_password, mobile)

        email_server = conf.get("email", "server")
        email_user = conf.get("email", "user")
        email_password = conf.get("email", "password")
        email_to = conf.get("email", "to")
        email_from = email_user

        email = Email(email_server, email_user, email_password,
            email_to, email_from)

        for identifier, tracking_data in cache.items():
            logging.info("processing tracking number %s", identifier)

            events = handle.query(identifier.strip())
            if not events: continue

            new_events = set(events) - set(tracking_data.events)
            if not new_events: continue

            for event in new_events:
                if tracking_data.desc:
                    msg = "Отправление %s [%s]: %s" % \
                        (identifier, tracking_data.desc, str(event))
                else:
                    msg = "Отправление %s: %s" % (identifier, str(event))

                send_notifications(sms, email, msg)
            
            cache[identifier].events = events
    else:
        run_shell(cache)

    save_cache(conf, cache)
    

if __name__ == '__main__':
    try:
        opts = parse_args()
        conf = parse_config(opts.config)

        init_logger(conf)
        main(opts, conf)
    except Exception as e:
        trace = traceback.format_exc()
        logging.error("%s\n%s\n", e, trace)

