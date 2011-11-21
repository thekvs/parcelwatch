# -*- coding: utf-8 -*-

import html5lib
import datetime
import urllib2
import urllib
import re

from StringIO import StringIO


class RussianPostTrackingEntry(object):
    
    def __init__(self, data):
        self.op = data[0]
        self.op_time = data[1]
        self.postal_code = data[2]
        self.post_office_name = data[3]
        self.op_attr = data[4]
        self.weight = data[5]
        self.value = data[6]
        self.payoff = data[7]
        self.dest_postal_code = data[8]
        self.dest_address = data[9]
        
    def __str__(self):
        s = ""
        if self.op_time:
            s += "%s: " % self.op_time
        if self.op:
            s += "%s " % self.op
        if self.postal_code and self.post_office_name:
            s += "(%s, %s)" % (self.postal_code, self.post_office_name)
        if self.op_attr:
            s += ", %s" % self.op_attr

        return s.encode('utf-8')


class RussianPostParser(object):

    get_statuses_xpath_expr = "//html:table[@class='pagetext']/html:tbody/html:tr[@align='center']"

    def __init__(self):
        self.parser = html5lib.HTMLParser(
            tree=html5lib.treebuilders.getTreeBuilder("lxml")
        )

    def __empty_search_results(self, data, barcode):
        rx_str = "К сожалению, информация о почтовом отправлении с номером %s не найдена." % barcode
        rx = re.compile(rx_str, re.IGNORECASE)

        if rx.search(data):
            return True
        else:
            return False

    def parse(self, data, barcode):
        document = self.parser.parse(StringIO(data))
        table = document.xpath(RussianPostParser.get_statuses_xpath_expr,
            namespaces={'html': 'http://www.w3.org/1999/xhtml'})
        resp = []

        if len(table) > 0:
            for row in table:
                data = []
                for cell in row.getchildren():
                    data.append(cell.text)
            
                resp.append(RussianPostTrackingEntry(data))
        elif not self.__empty_search_results(data, barcode):
            raise Exception("Unexpected HTML structure while quering for barcode %s" % barcode)

        return resp
        

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
        self.parser = RussianPostParser()

    def query(self, barcode):
        today = datetime.date.today()

        params = RussianPostQuery.default_query_params
        params["BarCode"] = barcode
        params["CYEAR"] = str(today.year)
        params["CMONTH"] = str(today.month)
        params["CDAY"] = str(today.day)

        req_data = urllib.urlencode(params)

        handle = urllib2.urlopen(RussianPostQuery.query_url, req_data)
        html = handle.read()    
        events = self.parser.parse(html, barcode)
            
        return events


if __name__ == "__main__":
    import sys
    import traceback

    from optparse import OptionParser

    parser = OptionParser()

    parser.add_option("", "--id", action="store",
        dest="id", help="tracking id")
    opts, args = parser.parse_args()

    if not opts.id:
        parser.error("Not enough args. given. Try --help switch for details.")

    try:
        handle = RussianPostQuery()
        events = handle.query(opts.id)

        if len(events) > 0:
            for event in events:
                print event
        else:
            print "No events."
    except Exception as e:
        trace = traceback.format_exc()
        print >>sys.stderr, "Oops: %s\n==============\n%s" % (e, trace)

