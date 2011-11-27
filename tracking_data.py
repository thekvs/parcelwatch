# -*- coding: utf-8 -*-

class TrackingData(object):

    def __init__(self, desc=None):
        self.events = []
        self.desc = desc

    def add_event(self, event):
        self.events.append(event)

    def description(self):
        if self.desc:
            return "[%s]" % self.desc
        else:
            return ""