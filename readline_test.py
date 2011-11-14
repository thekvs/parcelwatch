#!/usr/bin/env python
# -*- coding: utf-8 -*-

import readline

#values = ['aaa0',  'aaa1',  'aaa2',  'bbb_0', 'bbb_1', 'bbb_2',
#          'ccc-0', 'ccc-1', 'ccc-2', 'ddd?0', 'ddd?1', 'ddd?2']

level1_values = ['show', 'add', 'delete', 'tracking', 'save']
level2_values = ['events', 'delete']

def level1_completer(text, state):
    matches = [v for v in level1_values if v.startswith(text)]
    if len(matches) == 1 and matches[0] == text:
        # Add space if the current text is the same as the only match
        return "{} ".format(matches[0]) if state == 0 else None

    if state >= len(matches):
        return None

    return matches[state]


def level2_completer(text, state):
    matches = [v for v in level2_values if v.startswith(text)]
    if len(matches) == 1 and matches[0] == text:
        # Add space if the current text is the same as the only match
        return "{} ".format(matches[0]) if state == 0 else None

    if state >= len(matches):
        return None

    return matches[state]


def level1_parse_and_exec(cmd):
    cmd_parts = cmd.split()
    command = cmd_parts[0].lower()

    if len(cmd_parts) > 1:
        arg = cmd_parts[1]
    else:
        arg = None
    
    if command == 'tracking' and arg:

        saved_completer = readline.get_completer()
        readline.set_completer(level2_completer)

        while True:
            try:
                cmd = raw_input("  " + arg + "# ")
                level2_parse_and_exec(cmd)
            except EOFError:
                break
        
        readline.set_completer(saved_completer)

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


def level2_parse_and_exec(cmd):
    print "Level2: %s" % cmd


def main():    
    
    for line in ("tab: complete", "set show-all-if-unmodified on"):
        readline.parse_and_bind(line)

    readline.set_completer(level1_completer)

    while True:
        try:
            cmd = raw_input("parcelwatch> ")
            if len(cmd) == 0: continue
            level1_parse_and_exec(cmd)
        except EOFError:
            break

if __name__ == '__main__':
    main()