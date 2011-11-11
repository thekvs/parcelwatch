# -*- coding: utf-8 -*-

import urllib2
import urllib
import hashlib

from lxml import etree
from StringIO import StringIO

class ComtubeRuSMS(object):
    """For API description see http://bit.ly/vbo7OF"""

    api_base_url = "https://api.comtube.ru/scripts/sms_api/sendsms.php"

    def __init__(self, user, password, mobile):
        self.user = user
        self.password = password
        self.mobile = mobile

    def __validate_response(self, response):
        xml_stream = StringIO(response)
        tree = etree.parse(xml_stream)
        root = tree.getroot()

        try:
            code = int(root.find('code').text)
            desc = root.find('desc').text
        except ValueError as e:
            return (-1, "Couldn't convert to int: %s" % str(e))
        except AttributeError as e:
            return (-1, "Invalid XML: %s" % str(e))
        except Exception as e:
            return (-1, str(e))
        else:
            return (code, desc)

    def __sign(self, params):
        sorted_keys = sorted(list(params))
        url = ''

        for key in sorted_keys:
            url += key + '=' + urllib.quote_plus(params[key]) + '&'

        signature = hashlib.md5(url + '&password=' + urllib.quote_plus(self.password)).hexdigest()

        return signature

    def send(self, message):
        params = {'username': self.user, 'to': self.mobile, 'from': self.user,
            'message': message.decode('utf-8').encode('windows-1251')
        }

        params['signature'] = self.__sign(params)
        req_data = urllib.urlencode(params)

        try:
            handle = urllib2.urlopen(ComtubeRuSMS.api_base_url, req_data)
            response = handle.read()
        except Exception as e:
            (code, status_message) = (-1, "API query error: %s" % str(e))
        else:
            (code, status_message) = self.__validate_response(response)

        return (code, status_message)
