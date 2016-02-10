SteamPocalypse Readme


Summary:


Goals:




TODO:

    Tenatively done!
-Instanciate the Engine object within the engine.py file in order to allow the Object class to refer to it.  Either this, or come up with another solution.


-Split all map handling off into a seperate class called Level, with the possibility of adding an orver-arching World class to handle the multiple levels that could exist.  The new_game method in Engine would create the World object, and calls to the make_map method in Engine will create the Level objects as needed.  These object classes will contain every Tile that makes up their respective maps, as well as the lists of objects and actors they contain.









