########################################################
# The glue that holds all the other game elements together.  This file
# will handle input, call for the outcomes and draw the graphics.
########################################################


import libtcodpy as tcod

        
class Engine:
    def __init__(self):
    # Initializes the working parts of the game engine.
    # The game state will be set to the default, and the main
    # menu will be the first thing displayed...Once I code it.
        self.key = tcod.Key()
        self.mouse = tcod.Mouse()
        
    def render_all(self):
    # Renders everything in the game world, as needed.
        tcod.console_clear(0) # Start with a cleared console
        
        self.dun_level.player.check_fov()

        # Run through the entire map
        for y in range(self.dun_level.MAP_H):
            for x in range(self.dun_level.MAP_W):
                # If tile is in the player's FOV, draw it.
                if tcod.map_is_in_fov(self.dun_level.fov_map, x, y):
                    char = self.dun_level.map[x][y].char
                    tcod.console_set_default_foreground(0, tcod.white)
                    tcod.console_put_char(0, x, y, char, tcod.BKGND_NONE)
        
        # Run through the objects list, and draw everything
        for object in self.dun_level.objects:
            object.draw()
        
        # Draw all actors last, so they show up on top
        for actor in self.dun_level.actors:
            actor.draw()
        
        # Update the window to show all the changes
        tcod.console_flush()
       
    def handle_input(self):
    # Takes input from the player, be it keyboard or mouse.
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, 
            self.key, self.mouse)
        
        movement_keys = { tcod.KEY_KP8 : 'north',
                          tcod.KEY_KP9 : 'ne',
                          tcod.KEY_KP6 : 'east',
                          tcod.KEY_KP3 : 'se',
                          tcod.KEY_KP2 : 'south',
                          tcod.KEY_KP1 : 'sw',
                          tcod.KEY_KP4 : 'west',
                          tcod.KEY_KP7 : 'nw'    }
                          
        try:
            key_pressed = self.key.vk
            try_move = movement_keys[key_pressed]
            
            self.dun_level.player.move(try_move)
        except KeyError:
            pass
        
    def main_menu(self):
    # The title menu.  
    
    # This is the first thing you see and the interface
    # you use in between individual play sessions.  It will
    # provide the options for starting a new character, loading
    # a previous save, and changing settings.
        pass
        
    def play_menu(self):
    # This is the Esc menu that you access while in-game.
        pass
        
    def new_game(self):
    # Starts a new game, in a new world, with a new character.
        self.make_map()

    def make_map(self):
    # This will create the map as required.
    # This fuction will tie together orther helper functions in
    # order to create all the elements the map needs.  This includes
    # dungeons gen, spawning initial monsters, random items & features,
    # as well as any other bits that create the finished map.
        self.dun_level = Map()      
        self.dun_level.populate()
        self.dun_level.create_fov()


class Map:
# Holds all the information for a single dungeon level, or 1 map.
    def __init__(self):
        MAP_W = 80
        MAP_H = 50
        self.map = [ [ Tile('floor')
                        for y in range(MAP_H) ]
                            for x in range(MAP_W) ]
        
        self.map[20][20] = Tile('wall')
        self.map[25][25] = Tile('wall')
        
    def create_fov(self):
        self.fov_map = tcod.map_new (MAP_W, MAP_H)

        for y in range(MAP_H):
            for x in range(MAP_W):
                tcod.map_set_properties(fov_map, x, y, 
                    self.dun_level.map[x][y].transparent, 
                    self.dun_level.map[x][y].walkable)
        
    def populate(self):
        self.objects = []
        self.actors = []
        self.player = Object(10, 10, '@', 'Player', tcod.white)
        self.actors.append(self.player)
        
    def is_walkable(self, x, y):
        # First, make sure we won't end up off the map.
        if (x >= 0 and x <= MAP_W - 1 and 
            y >= 0 and y <= MAP_H - 1):
            return False
        # Find out if there is anything at a location that would block something.
        elif not self.map[x][y].walkable:
            return False
        
        for object in self.objects:
            if not object.walkable and object.x == x and object.y == y:
                return False
                
        for actor in self.actors:
            if not actor.walkable and actor.x == x and actor.y == y:
                return False
                    
        return True
        

class Tile:
# This is the map tile class.  It will know what type of tile it is,
# and feed this info up to the rendering functions.
# I would like to have varied terrain, and am considering
# using a variety of floors and walls in dungeon generation.  I'm
# currently unsure if this class will have to be moved over to
# the dungeon generation file to handle randomized dirt/grass colours,
# as well as the other features I'm hoping to see in the game. 
    def __init__(self, type):
        self.type = type    # This accepts a string
        types = {  'wall' : ('#', False, False),
                  'floor' : ('.', True, True)  }
        # Set the properties of a Tile based on it's type,
        # using the dict above to hold the properties of each type.
        self.char = types[self.type][0]
        self.walkable = types[self.type][1]
        self.transparent = types[self.type][2]        


class Object:
# The base "thing" or object in the game.  Everything that is not a tile
# belongs to this class.
    def __init__(self, x, y, char, name, colour, walkable=False):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.colour = colour
        self.walkable = walkable
        
    def draw(self):
        tcod.console_set_default_foreground(0, self.colour)
        tcod.console_put_char(0, self.x, self.y, self.char, tcod.BKGND_NONE)
        
    def move(self, direction):
        compass = {  'north' : (0, -1),
                        'ne' : (1, -1),
                      'east' : (1, 0),
                        'se' : (1, 1),
                     'south' : (0, 1),
                        'sw' : (-1, 1),
                      'west' : (-1, 0),
                        'nw' : (-1, -1)  }
        
        new_x = self.x + compass[direction][0]
        new_y = self.y + compass[direction][1]
        # Check with the map to see if a move is possible.
        if engine.dun_level.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
    
    def check_fov(self):
        tcod.map_compute_fov(fov_map, self.x, self.y, radius=0, 
            light_walls=True, algo=tcod.FOV_RESTRICTIVE)



        


