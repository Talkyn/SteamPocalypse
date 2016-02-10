###################################################################
#
# An Alchemy-themed, steampunk-pocalypse set roguelike.
#
# My first foray into banging rocks together in Python.  Most likely,
# it will never be very good.  Regardless of how long it may take, I
# intend to see it through to a playable state.  I have several
# quasi-unique ideas so the hope is I don't have a game that feels
# cloned from anything else.
#
###################################################################
#
# This is the main file, intended to be run in order to play the game.
# Most of the guts will be kept seperately.
#
###################################################################

import libtcodpy as tcod
import settings
import engine

class Game:
    def __init__(self):
        
        tcod.console_init_root(settings.SCREEN_W, settings.SCREEN_H, 'SteamPocalypse')
        tcod.sys_set_fps(20)
        

    def play_game(self):
        
        while not tcod.console_is_window_closed():

            engine.engine.handle_input()
            
            engine.engine.render_all()
            


session = Game()
session.play_game()