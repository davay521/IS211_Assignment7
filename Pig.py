"""David Vayman
IS211_Assignment7"""

import random
import time
import argparse

random.seed(0)  # set random seed for random.choice


class Player(object):
    """
    constructor: name,
                 current_roll_total = 0
    roll(x): calls random.choice on dice object(x)'s side attribute, updates
             current_roll_total and returns value to main game
    hold(y): updates scoreboard object(y) at end of turn and resets running total to 0
    """
    def __init__(self, playersName):
        self.name = playersName
        self.current_roll_total = 0

    def roll(self, diceName):
        throw = random.choice(diceName.sides)

        if throw > 1:           # updates current roll if score > 1
            self.current_roll_total += throw
        else:
            self.current_roll_total = 0     # resets current_roll total

        return throw    # return current throw to main for evaluation

    def hold(self, scoreboardName):

        scoreboardName.scoreboard[self.name] += self.current_roll_total    # updates scoreboard
        self.current_roll_total = 0                                         # resets current total



class Dice(object):

    """
 num_sides(default=6),
list comprehension that creates list with range 1 -> num_sides
    """

    def __init__(self, diceSides=6):
        self.sides = [diceSides for diceSides in range(1, diceSides + 1)]


class Scoreboard(object):
    """
    attribute: {} - key= Player name/ value = score(int)
    add_player(): creates a new key/value as:  'player name': 0,
    """
    def __init__(self):
        self.scoreboard = {}

    def add_player(self, player):

        self.scoreboard[player] = 0


## helper functions

def pause(seconds):
    """
    helper function... time.sleep wrapped in function to slow terminal output speed
    """

    return time.sleep(seconds)


def yes_or_no():
    """
    helper function... yes or no wrapped in error free while loop
    """
    switch = True
    while switch:

        user_input = str(raw_input("Please enter (Y) for Yes or (N) for No \n")).lower()

        if (user_input == 'y') or (user_input == 'n'):
            return user_input
        else:
            print "That is an Invalid response"


def enter_num_players():
    """
    helper function... yes or no wrapped in error free while loop
    this is used if the player/players want to replay the game
    """
    switch = True
    while switch:

        try:
            user_input = int(raw_input("Enter the number of players \n"))
            return user_input

        except ValueError:
            print "Invalid Response"




def makePlayers(num_players, scoreboard):
    """
    takes raw input from user/argparse and creates a list of player objects
    sets up the scoreboard with player names
    returns ordered list of players to main game
    """
    player_list = []

    for user in range(num_players):

        prompt = 'Player ' + str(user + 1) + '  Please enter your name: '
        user_name = str(raw_input(prompt))

        new_player = Player(user_name)
        player_list.append(new_player)
        scoreboard.add_player(new_player.name)

    return player_list

# main game function
def game_engine(player_list, scoreboard, game_dice):
    """
    main game sequence...   outer while loop - continues cycling players until someone wins (return True)
                            for loop - moves through the players in the player list
                            inner while loop - game algorithm -- returns True to main when there is a winner
    """
    while True:     # outer loop -- always on until somebody wins

        for player in player_list:

            while player:

                print player.name.upper() + ' It your turn'
                pause(1)
                user_input = str(raw_input(player.name + ', What would you like to do ? Roll or Hold? Please enter (r)for Roll or (h) for Hold: ')).lower()

                if user_input == 'r':

                    roll = player.roll(game_dice)
                    print player.name.upper() + ' rolled a ' + str(roll) + ' !!'
                    print ''
                    pause(1)

                    if roll > 1:

                        shadow_total = player.current_roll_total + scoreboard.scoreboard[player.name]

                        if shadow_total >= 100:
                            print player.name.upper() + 's: total for this roll = ' + str(player.current_roll_total)
                            pause(1)
                            print player.name.upper() + 's: GRAND TOTAL: ' + str(shadow_total)
                            print ''
                            pause(1)
                            return player.name      # EXITS function here on WINNER, returns name to main
                        else:
                            print player.name.upper() + 's:total for this roll = ' + str(player.current_roll_total)
                            pause(1)
                            print player.name.upper() + 's:GRAND TOTAL: ' + str(shadow_total)
                            print ''
                            pause(1)

                    else:
                        print 'OH NO!!' + player.name + ' ... all points this roll are lost!!'
                        pause(1)
                        print ''
                        print '______________'
                        print '<><><><><><><>'
                        print 'CURRENT SCORES: ' + str(scoreboard.scoreboard)
                        print '<><><><><><><>'
                        print '______________'
                        print ''
                        print ''
                        break


                elif user_input == 'h':
                    player.hold(scoreboard)    # calls hold method then breaks out of loop
                    print player.name + ':: chooses to hold'
                    pause(1)
                    print ''
                    print '______________'
                    print '<><><><><><><>'
                    print 'CURRENT SCORES: ' + str(scoreboard.scoreboard)
                    print '<><><><><><><>'
                    print '______________'
                    print ''
                    break
                else:
                    print 'Invalid Please TRY AGAIN '
                    print ''
                    pause(.5)


def main():
    """
    main script::
        1. gets initial user input from argparse for number of players
        encapsulate in while loop
            2. Instantiates Dice and Scoreboard instances for current game
            3. calls makePlayers to get player list for current game
            4. calls game_engine to play game
            5. when game ends asks player to play again or exit
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--numPlayers", help="number of players for the game")
    args = parser.parse_args()

    try:

        num_players = int(args.numPlayers)

        game_switch = True
        while game_switch:

            game_dice = Dice()
            game_scoreboard = Scoreboard()

            player_list = makePlayers(num_players, game_scoreboard)
            winner = game_engine(player_list, game_scoreboard, game_dice)

            print winner + "!!!YOU ARE THE WINNER!!!"
            pause(2)

            print 'Would you like to play again?'
            pause(1)

            response = yes_or_no()

            if response != 'y':

                print 'Thanks for playing!!'
                game_switch = False

            else:
                num_players = enter_num_players()

    except TypeError:
        print "Please enter the number(interger) of player next ro the --numPlayer argument"



if __name__ == "__main__":
    main()


