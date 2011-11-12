# -*- coding: utf-8 -*-

import html5lib
import datetime
import urllib2
import urllib

class RussianPostTrackingEntry(object):
    pass

class RussianPostQuery(object):

    query_url = "http://russianpost.ru/resp_engine.aspx?Path=rp/servise/ru/home/postuslug/trackingpo"
    default_query_params = {
        "OP": "",
        "PATHCUR": "rp/servise/ru/home/postuslug/trackingpo",
        "PATHFROM": "",
        "WHEREONOK": "",
        "ASP": "",
        "PARENTID": "",
        "FORUMID": "",
        "NEWSID": "",
        "DFROM": "",
        "DTO": "",
        "CA": "",
        "NAVCURPAGE": "",
        "SEARCHTEXT": "",
        "searchbarcode": "Найти",
        "searchsign": "1"
    }

    def __init__(self):
        pass

    def query(self, barcode):
        today = datetime.date.today()

        params = RussianPostQuery.default_query_params
        params["BarCode"] = barcode
        params["CYEAR"] = str(today.year)
        params["CMONTH"] = str(today.month)
        params["CDAY"] = str(today.day)

        response = ""
        req_data = urllib.urlencode(params)

        try:
            handle = urllib2.urlopen(RussianPostQuery.query_url, req_data)
            response = handle.read()
        except Exception as e:
            response = "Error: %s" % e
            
        return response


class RussianPostParser(object):

    def __init__(self):
        self.handle = RussianPostQuery()
    

if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("", "--id", action="store",
        dest="id", help="tracking id")
    opts, args = parser.parse_args()

    if not opts.id:
        parser.error("Not enough args. given. Try --help switch for details.")

    handle = RussianPostQuery()
    resp = handle.query(opts.id)

    print resp
