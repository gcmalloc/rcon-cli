#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import valve.source.rcon
import logging
from colorama import init
import os
import argparse
from colorama import Fore, Back, Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory



DEFAULT_PORT = 27015


def get_parser():
    """docstring for get_parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help="ip:port tuple to connect to the server. default port is 27015")
    parser.add_argument('-p', '--password', default='')
    parser.add_argument('SCRIPT', nargs='?')
    return parser


class MyCustomCompleter(Completer):
    def __init__(self, con):
        """docstring for __init__"""
        self.con = con

    def get_completions(self, document, complete_event):
        if document.text == '' or ' ' in document.text:
            return
        results = self.con('find {}'.format(document.text))
        for result in results.split('\n'):
            if '"' in result:
                command_result = result.split('"')[1].strip()
                if '-' in result:
                    command_help = result.split('-')[1].strip()
                else:
                    command_help = ''
                if command_result.startswith(document.text):
                    yield Completion(result.split('"')[1], start_position=-len(document.text), display_meta=command_help)


def shell(host, port, password):
    history = FileHistory(os.path.expanduser('~/.rcon_shell'))
    with valve.source.rcon.RCON((host, int(port)), parsed_args.password) as con:
        while 1:
            try:
                text = prompt(u"rcon {}:{}>".format(host, port), completer=MyCustomCompleter(con), history=history)
            except KeyboardInterrupt:
                print("Closing Rcon connection and exiting")
                exit(0)
            print(Fore.GREEN + con(text))


def exec_script(host, port, password, f):
    with valve.source.rcon.RCON((host, int(port)), parsed_args.password) as con:
        with open(f) as shell_file:
            for command in shell_file.readlines():
                print(con(command))
    
if __name__ == '__main__':
    init()
    parser = get_parser()
    parsed_args = parser.parse_args()
    logging.debug(parsed_args)
    splitted_url = parsed_args.url.split(':')
    if len(splitted_url) == 2:
        host, port = splitted_url
    else:
        host, port = splitted_url, DEFAULT_PORT
    password = parsed_args.password
    if parsed_args.SCRIPT:
        exec_script(host, port, password, parsed_args.SCRIPT)
    else:
        shell(host, port, password)
