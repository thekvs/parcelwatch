#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline

values = [['show', 'add', 'delete', 'tracking', 'save'], ['events', 'delete']]


def completer(text, state):
    matches = [v for v in values[level] if v.startswith(text)]
    if len(matches) == 1 and matches[0] == text:
        # Add space if the current text is the same as the only match
        return "{} ".format(matches[0]) if state == 0 else None

    if state >= len(matches):
        return None

    return matches[state]


def parse_and_exec_0(command, arg):
    if command == 'tracking' and arg:
        global level
        level = 1

        while True:
            try:
                cmd = raw_input("  " + arg + "# ")
                parse_and_exec(cmd)
            except EOFError:
                print
                break
        
        level = 0
    elif command == 'show':
        print "Executing 'show' command"
    elif command == 'save':
        print "Executing 'save' command"
    elif command == 'add' and arg:
        print "Executing 'add' command with argument '%s'" % arg
    elif command == 'delete' and arg:
        print "Executing 'delete' command with argument '%s'" % arg
    else:
        print "Unknown command and arg: (%s, %s)" % (command, arg)


def parse_and_exec_1(command, arg):
    print "Level2: cmd=%s, arg=%s" % (command, arg)


def parse_and_exec(cmd):
    cmd_parts = cmd.split()
    command = cmd_parts[0].lower()

    if len(cmd_parts) > 1:
        arg = cmd_parts[1]
    else:
        arg = None

    if level == 0:
        parse_and_exec_0(command, arg)
    else:
        parse_and_exec_1(command, arg)


def main():    
    
    for line in ("tab: complete", "set show-all-if-unmodified on"):
        readline.parse_and_bind(line)

    readline.set_completer(completer)

    global level
    level = 0

    while True:
        try:
            cmd = raw_input("parcelwatch> ")
            if len(cmd) == 0: continue
            parse_and_exec(cmd)
        except EOFError:
            print
            break


if __name__ == '__main__':
    main()