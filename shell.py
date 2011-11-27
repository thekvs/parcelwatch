# -*- coding: utf-8 -*-

import readline
import re

from tracking_data import TrackingData

values = [['show', 'add', 'delete', 'tracking'], ['show', 'delete', 'desc']]

internal_tracking_vrf_rx = re.compile("^\d{14}$")
international_tracking_vrf_rx = re.compile("^[A-Z]{2}\d{9}[A-Z]{2}$")


def completer(text, state):
    matches = [v for v in values[level] if v.startswith(text)]
    if len(matches) == 1 and matches[0] == text:
        # Add space if the current text is the same as the only match
        return "{} ".format(matches[0]) if state == 0 else None

    if state >= len(matches):
        return None

    return matches[state]


def parse_and_exec_0(command, arg, ctx):
    cache = ctx
    if command == 'tracking' and arg:
        run_tracking_cmd(cache, arg)
    elif command == 'show':
        run_show_cmd(cache)
    elif command == 'add' and arg:
        run_add_cmd(cache, arg)
    elif command == 'delete' and arg:
        run_delete_cmd(cache, arg)
    else:
        print "(0) Error: unknown command and arg: (%s, %s)" % (command, arg)


def parse_and_exec_1(command, arg, ctx):
    if command == 'show':
        run_show_events_cmd(ctx)
    elif command == 'delete' and arg:
        run_delete_event_cmd(ctx, arg)
    elif command == 'desc':
        run_desc_event_cmd(ctx, arg)
    else:
        print "(1) Error: unknown command and arg: (%s, %s)" % (command, arg)


def parse_and_exec(input_data, ctx):
    parts = input_data.split()
    command = parts[0].lower()

    if len(parts) > 1:
        if len(parts) > 2:
            arg = ' '.join(parts[1:])
        else:
            arg = parts[1]
    else:
        arg = None

    if level == 0:
        parse_and_exec_0(command, arg, ctx)
    else:
        parse_and_exec_1(command, arg, ctx)


def verify_barcode(barcode):
    if international_tracking_vrf_rx.search(barcode):
        return True
    elif internal_tracking_vrf_rx.search(barcode):
        return True
    else:
        return False


def run_show_cmd(cache):
    index = 0
    for key, value in cache.iteritems():
        s = "  #%i:%18s" % (index, key)
        desc = value.description()
        if desc:
            s += " -- %s" % desc
        print s
        index += 1


def run_add_cmd(cache, barcode):
    if cache.has_key(barcode):
        print "Error: tracking number \"%s\" already exists" % barcode
    elif verify_barcode(barcode):
        cache[barcode] = TrackingData()
        print "Ok"
    else:
        print "Error: invalid tracking number \"%s\" format" % barcode


def run_delete_cmd(cache, number):
    try:
        index = int(number)
    except Exception as e:
        print "Error: couldn't convert \"%s\" to integer" % number
    else:
        if index < 0 or index >= len(cache):
            print "Error: invalid index %i" % index
        else:
            keys = cache.keys()
            del cache[keys[index]]
            print "Ok"


def run_tracking_cmd(cache, number):
    try:
        index = int(number)
    except Exception as e:
        print "Error: couldn't convert \"%s\" to integer" % number
    else:
        barcodes = cache.keys()
        if index < 0 or index >= len(barcodes):
            print "Error: invalid index %i" % index
        else:
            barcode = barcodes[index]    
            ctx = cache[barcode]
            global level
            level = 1

            while True:
                try:
                    input_data = raw_input("  " + barcode + "# ")
                    if len(input_data) == 0: continue
                    parse_and_exec(input_data, ctx)
                except EOFError:
                    print
                    break
            
            level = 0
            
            
def run_show_events_cmd(ctx):
    for index, event in enumerate(ctx.events):
        print "    #%i: %s" % (index, event)


def run_delete_event_cmd(ctx, number):
    try:
        index = int(number)
    except Exception as e:
        print "Error: couldn't convert \"%s\" to integer" % number
    else:
        if len(ctx.events) == 0 or index < 0 or index >= len(ctx.events):
            print "Error: invalid index %i" % index
        else:
            del ctx.events[index]


def run_desc_event_cmd(ctx, desc):
    ctx.desc = desc
    print "  Ok"


def run_shell(cache):    
    for line in ("tab: complete", "set show-all-if-unmodified on"):
        readline.parse_and_bind(line)

    readline.set_completer(completer)

    global level
    level = 0

    while True:
        try:
            input_data = raw_input("parcelwatch> ")
            if len(input_data) == 0: continue
            parse_and_exec(input_data, cache)
        except EOFError:
            print
            break

