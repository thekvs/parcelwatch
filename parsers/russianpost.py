# -*- coding: utf-8 -*-

import html5lib
import datetime
import urllib2
import urllib

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

    def __repr__(self):
        s = "%s: %s (%s, %s), %s" % (self.op_time, self.op, self.postal_code,
            self.post_office_name, self.op_attr)
        return s.encode('utf-8')


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

    __xpath_expr = "//html:table[@class='pagetext']/html:tbody/html:tr[@align='center']"

    def __init__(self):
        self.parser = html5lib.HTMLParser(
            tree=html5lib.treebuilders.getTreeBuilder("lxml")
        )

    def parse(self, data):
        document = self.parser.parse(StringIO(data))
        table = document.xpath(RussianPostParser.__xpath_expr,
            namespaces={'html': 'http://www.w3.org/1999/xhtml'})
        resp = []
        
        for row in table:
            data = []
            for cell in row.getchildren():
                data.append(cell.text)
        
            resp.append(RussianPostTrackingEntry(data))

        return resp
        

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

