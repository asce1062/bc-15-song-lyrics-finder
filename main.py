#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Song Lyrics Finder
MusixMatch API.
As a user, I can perform the following operations:
find <search_query_string> - Returns a list of songs that match the criteria.
view <song_id> - View song lyrics based on its ID. Optimized to check for local copy first.
save <song_id> - store song details and lyrics locally
clear - clear the entire local database
"""
import cmd
import os
from docopt import docopt, DocoptExit
import string

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
    # clear terminal first.
    os.system('cls' if os.name == 'nt' else 'clear')
    # Andela logo from
    # https://www.movemeback.com/opportunities/andela-role-in-technology/

    print colored.cyan('                   O8', bold=12)
    print colored.cyan('                  @@@@C', bold=12)
    print colored.cyan('                @@@@@@@@c', bold=12)
    print colored.cyan('      @@@@@@@@O8@@8  8@@8o@@@@@@@@c', bold=12)
    print colored.cyan('      @@@@@@@@            C@@@@@@@c', bold=12)
    print colored.cyan('      8@@8                    8@@@                     O@@                                   8@@c                o@@O', bold=12)
    print colored.cyan('      O@@@                    @@@8                     @@@O                                  8@@c                o@@O', bold=12)
    print colored.cyan('      C                          C                    @@@@@8                                 8@@c                o@@O', bold=12)
    print colored.cyan('   o@@@@                        o@@@o                @@@ o@@8      C@@CO@@@@@@8     c@@@@@@@@@@@c   c@@@@@@@@o   o@@O     8@@@@@@@@8', bold=12)
    print colored.cyan(' c@@@@@C                         @@@@@O             8@@c  @@@      C@@@@8ocC@@@8   O@@@C   8@@@@c  8@@@Cc o@@@C  o@@O     @@C   cO@@@c', bold=12)
    print colored.cyan('c@@@@@c                           8@@@@o           o@@O    @@@     C@@8      O@@C C@@C       @@@c O@@c      o@@C o@@O             o@@C', bold=12)
    print colored.cyan('   @@@@@o                       8@@@@c            o@@8oooooo@@@    C@@C      o@@O 8@@c       8@@c @@@@@@@@@@@@@8 o@@O     @@@@@@@@@@@C', bold=12)
    print colored.cyan('     O@o                         @@o             c@@@@@@@@@@@@@8   C@@C      o@@O O@@c       8@@c @@@8888888888O o@@O   c@@@c     o@@C', bold=12)
    print colored.cyan('      O@@O                    O8@O               @@@         8@@o  C@@C      o@@O c@@@      C@@@c C@@8       Oc  o@@O   o@@C      O@@C', bold=12)
    print colored.cyan('      8@@@                    8@@@              8@@o          O@@o C@@C      o@@O   @@@@@@@@@@@@c  c@@@@@@@@@@8   @@@@@  O@@@@@@@@@@@@o', bold=12)
    print colored.cyan('      @@@@O88O            c@8O8@@@             oOOo            OOO cOOo      cOOo    cO@@@@C COO     cC8@@@Oo      c888   cO8@@@C  O88o', bold=12)
    print colored.cyan('      @@@@@@@@CcO@o  c@@c 8@@@@@@@c', bold=12)
    print colored.cyan('      cocc     @@@@8o@@@@c    ccoc', bold=12)
    print colored.cyan('                 8@@@@@C', bold=12)
    print colored.cyan('                  o@@o', bold=12)
    print ("")
    print ("")
    print colored.cyan("                          ___                  _              _            ___  _         _           ", bold=12)
    print colored.cyan("                         / __> ___ ._ _  ___  | |   _ _  _ _ <_> ___  ___ | __><_>._ _  _| | ___  _ _ ", bold=12)
    print colored.cyan("                         \__ \/ . \| ' |/ . | | |_ | | || '_>| |/ | '<_-< | _> | || ' |/ . |/ ._>| '_>", bold=12)
    print colored.cyan("                         <___/\___/|_|_|\_. | |___|`_. ||_|  |_|\_|_./__/ |_|  |_||_|_|\___|\___.|_|  ", bold=12)
    print colored.cyan("                                        <___'      <___'                                              ", bold=12)
    print ("")
    print ("")
    print colored.cyan("                                                 +--------------------------------+", bold=12)
    print colored.cyan("                                                 |        Song Lyrics Finder      |", bold=12)
    print colored.cyan("                                                 |--------------------------------|", bold=12)
    print colored.cyan("                                                 |Command |   Input   |  Example  |", bold=12)
    print colored.cyan("                                                 |--------------------------------|", bold=12)
    print colored.cyan("                                                 |find    | Song_name |    BYOB   |", bold=12)
    print colored.cyan("                                                 |view    |  SongID   |  3657996  |", bold=12)
    print colored.cyan("                                                 |save    |  SongID   |  3657996  |", bold=12)
    print colored.cyan("                                                 |clear   |   clear   |    N/A    |", bold=12)
    print colored.cyan("                                                 |--------------------------------|", bold=12)
    print colored.cyan('                                                 |  type "help" to view commands  |', bold=12)
    print colored.cyan("                                                 |--------------------------------|", bold=12)
    print colored.cyan('                                                 |type "help command" for  syntax |', bold=12)
    print colored.cyan("                                                 +--------------------------------+", bold=12)

    prompt = colored.magenta("\nasce1062") + \
        colored.cyan("@") + \
        colored.yellow("AlexImmers-MacBook-Pro") + \
        colored.red(":") + \
        colored.cyan("~/bc-15-song-lyrics-finder") + \
        colored.red("|") + \
        colored.green("master") + \
        colored.yellow("⚡") + \
        colored.cyan("\n⇒")

    @docopt_cmd
    def do_find(self, arg):
        """
        Usage: find <song_name>
        """
        query = arg["<song_name>"]

        # clear terminal first.
        os.system('cls' if os.name == 'nt' else 'clear')
        search(query)

    @docopt_cmd
    def do_view(self, arg):
        """
        Usage: view <trackid>
        """
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            track_id = arg["<trackid>"]
            assert any(
                [char not in string.ascii_letters for char in track_id]) is True
        except AssertionError:
            print colored.red("Usage: view <track_id> MUST consist of integers only", bold=12)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            song_view(track_id)

    @docopt_cmd
    def do_save(self, arg):
        """
        Usage: save <trackid>
        """
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            track_id = arg["<trackid>"]
            assert any(
                [char not in string.ascii_letters for char in track_id]) is True
        except AssertionError:
            print colored.red("Usage: save <track_id> MUST consist of integers only", bold=12)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            song_save(track_id)

    @docopt_cmd
    def do_clear(self, arg):
        """
        Usage: clear
        """
        # clear terminal first.
        os.system('cls' if os.name == 'nt' else 'clear')
        song_clear()

    def do_quit(self, arg):
        """
        Quits out of Interactive Mode.
        """
        # clear terminal first.
        os.system('cls' if os.name == 'nt' else 'clear')
        print colored.red('Goodbye.', bold=12)
        time.sleep(3)  # delays for 3 seconds
        # clear terminal first.
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(0.25)  # delays for 0.3 seconds
        print colored.magenta('                           oooo$$$$$$$$$$$$oooo', bold=12)
        time.sleep(0.25)  # delays for 0.3 seconds
        print colored.magenta('                       oo$$$$$$$$$$$$$$$$$$$$$$$$o', bold=12)
        time.sleep(0.25)  # delays for 0.3 seconds
        print colored.magenta('                    oo$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$o         o$   $$ o$', bold=12)
        time.sleep(0.25)  # delays for 0.3 seconds
        print colored.magenta('    o $ oo        o$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$o       $$ $$ $$o$', bold=12)
        time.sleep(0.25)  # delays for 0.3 seconds
        print colored.magenta(' oo $ $ "$      o$$$$$$$$$    $$$$$$$$$$$$$    $$$$$$$$$o       $$$o$$o$', bold=12)
        time.sleep(0.25)  # delays for 0.3 seconds
        print colored.magenta(' "$$$$$$o$     o$$$$$$$$$      $$$$$$$$$$$      $$$$$$$$$$o    $$$$$$$$', bold=12)
        time.sleep(0.25)  # delays for 0.3 seconds
        print colored.magenta('   $$$$$$$    $$$$$$$$$$$      $$$$$$$$$$$      $$$$$$$$$$$$$$$$$$$$$$$', bold=12)
        time.sleep(0.25)  # delays for 0.3 seconds
        print colored.magenta('   $$$$$$$$$$$$$$$$$$$$$$$    $$$$$$$$$$$$$    $$$$$$$$$$$$$$  """$$$', bold=12)
        time.sleep(0.25)  # delays for 0.3 seconds
        print colored.magenta('    "$$$""""$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     "$$$', bold=12)
        time.sleep(0.25)  # delays for 0.3 seconds
        print colored.magenta('     $$$   o$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     "$$$o', bold=12)
        time.sleep(0.25)  # delays for 0.3 seconds
        print colored.magenta('    o$$"   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$       $$$o', bold=12)
        time.sleep(0.25)  # delays for 0.3 seconds
        print colored.magenta('    $$$    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$" "$$$$$$ooooo$$$$o', bold=12)
        time.sleep(0.25)  # delays for 0.3 seconds
        print colored.magenta('   o$$$oooo$$$$$  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$   o$$$$$$$$$$$$$$$$$', bold=12)
        time.sleep(0.25)  # delays for 0.3 seconds
        print colored.magenta('   $$$$$$$$"$$$$   $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     $$$$""""""""', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.magenta('  """"       $$$$    "$$$$$$$$$$$$$$$$$$$$$$$$$$$$"      o$$$', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.magenta('             "$$$o     """$$$$$$$$$$$$$$$$$$"$$"         $$$', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.magenta('               $$$o          "$$""$$$$$$""""           o$$$', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.magenta('                $$$$o                 oo             o$$$"', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.magenta('                 "$$$$o      o$$$$$$o"$$$$o        o$$$$', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.magenta('                   "$$$$$oo     ""$$$$o$$$$$o   o$$$$""', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.magenta('                      ""$$$$$oooo  "$$$o$$$$$$$$$"""', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.magenta('                         ""$$$$$$$oo $$$$$$$$$$', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.magenta('                                 """"$$$$$$$$$$$', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.magenta('                                     $$$$$$$$$$$$', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.magenta('                                      $$$$$$$$$$"', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.magenta('                                       "$$$""""', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.cyan('                                              ___                       ___', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.cyan('                                             /\  \          ___        /\  \\', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.cyan('                                             \:\  \        /\  \      /::\  \\', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.cyan('                                              \:\  \       \:\  \    /:/\:\  \\', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.cyan('                                              /::\  \      /::\__\  /::\~\:\  \\', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.cyan('                                             /:/\:\__\  __/:/\/__/ /:/\:\ \:\__\\', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.cyan('                                            /:/  \/__/ /\/:/  /    \/__\:\/:/  /', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.cyan('                                           /:/  /      \::/__/          \::/  /', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.cyan('                                           \/__/        \:\__\          /:/  /', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.cyan('                                                         \/__/         /:/  /', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        print colored.cyan('                                                                       \/__/', bold=12)
        time.sleep(0.3)  # delays for 0.3 seconds
        exit()


if __name__ == '__main__':
    SongLyricsFinder().cmdloop()
