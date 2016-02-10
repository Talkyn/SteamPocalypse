#Experiments with dice rolling
#
#This dice roller is capable of handling a typical RPG dice roll, including an optional bonus
#eg 2d6+2
#

import random


def roll_dice(roll):
    #Take a string for a normal RPG dice roll and simulate actually rolling said dice and adding them all up
    result = 0
    dice = 0
    die = 0
    bonus = 0

    try:
        bonus = int(roll.split("+")[1])
        roll = roll.split("+")[0]
    
        dice = int(roll.split("d")[0])
        die = int(roll.split("d")[1])
    
        while dice > 0:
            result += random.randint(1, die)
            dice -= 1

        result += bonus
        print result
        
    except IndexError:
    
        dice = int(roll.split("d")[0])
        die = int(roll.split("d")[1])
    
        while dice > 0:
            result += random.randint(1, die)
            dice -= 1

        result += bonus
        print result

while True:

    print("Hello!  Please type in a typical RPG dice roll, eg '1d6' or '2d8+3'")
    roll = raw_input("Please roll these dice: ")

    try:
        roll_dice(roll)
    except:
        print("Hmm...That doesn't make sense.  Try again! ")
