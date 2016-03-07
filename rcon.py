#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import logging
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
import os
import argparse
from srcds.rcon import RconConnection
import cmd


DEFAULT_PORT = 27015


def get_parser():
    """docstring for get_parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help="ip:port tuple to connect to the server. default port is 27015")
    parser.add_argument('-p', '--password', default='')
    parser.add_argument('FILE', nargs='?')
    return parser

if __name__ == '__main__':
    parser = get_parser()
    parsed_args = parser.parse_args()
    logging.debug(parsed_args)
    splitted_url = parsed_args.url.split(':')
    if len(splitted_url) == 2:
        host, port = splitted_url
    else:
        host, port = splitted_url, DEFAULT_PORT
    con = RconConnection(host, port, parsed_args.password)
    while 1:
        try:
            text = prompt(u"rcon {}:{}>".format(host, port))
        except KeyboardInterrupt:
            print("Closing Rcon connection and exiting")
        print(con.exec_command(text))
