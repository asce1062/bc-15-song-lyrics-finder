# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
Song Lyrics Finder
For this project, I have made use of MusixMatch API or RapGenius API.
As a user, I can perform the following operations:
song find <search_query_string> - Returns a list of songs that match the criteria.
song vie <song_id> - View song lyrics based on its ID. Optimized to check for local copy first.
song save <song_id> - store song details and lyrics locally
song clear - clear the entire local databse
"""
import cmd

from clint.textui import colored
from docopt import docopt, DocoptExit

from song_lyrics_finder import *


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class SongLyricsFinder(cmd.Cmd):
    print colored.cyan("  .::                                            .::::::::                 .::                 ", bold=12)
    print colored.cyan("  .::                       .:                   .::       .:              .::                 ", bold=12)
    print colored.cyan("  .::      .::   .::.: .:::      .::: .::::      .::         .:: .::       .::   .::    .: .:::", bold=12)
    print colored.cyan("  .::       .:: .::  .::   .:: .::   .::         .::::::  .:: .::  .:: .:: .:: .:   .::  .::   ", bold=12)
    print colored.cyan("  .::         .:::   .::   .::.::      .:::      .::      .:: .::  .::.:   .::.::::: .:: .::   ", bold=12)
    print colored.cyan("  .::          .::   .::   .:: .::       .::     .::      .:: .::  .::.:   .::.:         .::   ", bold=12)
    print colored.cyan("  .::::::::   .::   .:::   .::   .:::.:: .::     .::      .::.:::  .:: .:: .::  .::::   .:::   ", bold=12)
    print colored.cyan("            .::", bold=12)

    print colored.cyan("                                +--------------------------------+", bold=12)
    print colored.cyan("                                |        Song Lyrics Finder      |", bold=12)
    print colored.cyan("                                |--------------------------------|", bold=12)
    print colored.cyan("                                |Command |   Input   | Parameter |", bold=12)
    print colored.cyan("                                |--------------------------------|", bold=12)
    print colored.cyan("                                |find    | song name |    BYOB   |", bold=12)
    print colored.cyan("                                |view    |  Song ID  |  3657996  |", bold=12)
    print colored.cyan("                                |save    |  Song ID  |  3657996  |", bold=12)
    print colored.cyan("                                |clear   |   clear   |    N/A    |", bold=12)
    print colored.cyan("                                |--------------------------------|", bold=12)
    print colored.cyan('                                |  type "help" to view commands  |', bold=12)
    print colored.cyan("                                +--------------------------------+", bold=12)
    prompt = colored.green("Alex.Immer@ANDELA-BOOT CAMP ~ \n$ ", bold=12)

    @docopt_cmd
    def do_find(self, arg):
        """Usage: find <query> """
        query = arg["<query>"]
        search(query)

    @docopt_cmd
    def do_view(self, arg):
        """Usage: view <track_id>"""
        track_id = arg["<track_id>"]
        if track_id.isalpha():
            print "Track id should contain numbers only"
        song_view(track_id)

    @docopt_cmd
    def do_save(self, arg):
        """Usage: save <track_id>"""
        track_id = arg["<track_id>"]
        if track_id.isalpha():
            print "track id should contain numbers only"
        song_save(track_id)

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print colored.red('Booo...', bold=12)
        exit()


if __name__ == '__main__':
    SongLyricsFinder().cmdloop()
