# -*- coding: utf-8 -*-

import readline

values = [['show', 'add', 'delete', 'tracking'], ['show', 'delete']]


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
    events = ctx
    if command == 'show':
        run_show_events_cmd(events)
    elif command == 'delete' and arg:
        run_delete_event_cmd(events, arg)
    else:
        print "(1) Error: unknown command and arg: (%s, %s)" % (command, arg)


def parse_and_exec(input_data, ctx):
    parts = input_data.split()
    command = parts[0].lower()

    if len(parts) > 1:
        arg = parts[1]
    else:
        arg = None

    if level == 0:
        parse_and_exec_0(command, arg, ctx)
    else:
        parse_and_exec_1(command, arg, ctx)


def verify_barcode(barcode):
    # TODO
    return True


def run_show_cmd(cache):
    for index, key in enumerate(cache.iterkeys()):
        print "  #%i:    %s" % (index, key)


def run_add_cmd(cache, barcode):
    if cache.has_key(barcode):
        print "Error: tracking number %s already exists" % barcode
    elif verify_barcode(barcode):
        cache[barcode] = []
        print "Ok"
    else:
        print "Error: invalid tracking number %s format" % barcode


def run_delete_cmd(cache, number):
    try:
        index = int(number)
    except Exception as e:
        print "Error: couldn't convert %s to integer" % number
    else:
        if index < 0 or index > len(cache):
            print "Error: invalid index number %s" % number
        else:
            keys = cache.keys()
            del cache[keys[index]]
            print "Ok"


def run_tracking_cmd(cache, number):
    try:
        index = int(number)
    except Exception as e:
        print "Error: couldn't convert %s to integer" % number
    else:
        barcodes = cache.keys()
        if index < 0 or index > len(barcodes):
            print "Error: invalid index %s" % number
        else:
            barcode = barcodes[index]
            if verify_barcode(barcode):
                if cache.has_key(barcode):
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
                else:
                    print "Error: tracking number %s is not registered" % barcode
            else:
                print "Error: invalid tracking number"


def run_show_events_cmd(events):
    for index, event in enumerate(events):
        print "    #%i: %s" % (index, event)


def run_delete_event_cmd(events, number):
    try:
        index = int(number)
    except Exception as e:
        print "Error: couldn't convert %s to integer" % number
    else:
        if len(events) == 0 or index < 0 or index >= len(events):
            print "Error: invalid index %s" % number
        else:
            del events[index]


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

