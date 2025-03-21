# Jacobus Burger (2024)
# MENACE (short for Matchbox Educable Noughts and Crosses Engine) was
#   an early convolutional neural network. This program is a replication
#   of the basic principle of MENACE in Python 3.
# see: https://en.wikipedia.org/wiki/Matchbox_Educable_Noughts_and_Crosses_Engine
from __init__ import *
from time import sleep
from random import choice, randint


DELAY = 0.5  # number of seconds to wait before displaying MENACE's move
CHAR_MAP = {
    NO_ONE: ' ',
    MENACE: 'O',
    PLAYER: 'X',
}


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def board_string(board_state):
    return ''.join(CHAR_MAP[n] for n in board_state)


def show_board(generation, board_state):
    clear()
    print("===== MENACE gen {} =====".format(generation))
    board = board_string(board_state)
    for i in range(2):
        print('|'.join(board[i * 3 : i * 3 + 3]))
        print("-+-+-")
    print('|'.join(board[6:9]))


def winning_player(board_state):
    # I love snake lang 🐍
    for i in range(3):
        # check for rows
        if all(state == MENACE for state in board_state[i * 3 : i * 3 + 3]):
            return MENACE
        if all(state == PLAYER for state in board_state[i * 3 : i * 3 + 3]):
            return PLAYER
        # check for columns
        if all(state == MENACE for state in board_state[i :: 3]):
            return MENACE
        if all(state == PLAYER for state in board_state[i :: 3]):
            return PLAYER
    # check for diagonals
    #   check top-right to bottom-left
    if all(state == MENACE for state in board_state[2 : 7 : 2]):
        return MENACE
    if all(state == PLAYER for state in board_state[2 : 7 : 2]):
        return PLAYER
    #   check top-left to bottom-right
    if all(state == MENACE for state in board_state[0 :: 4]):
        return MENACE
    if all(state == PLAYER for state in board_state[0 :: 4]):
        return PLAYER
    return NO_ONE


def main():
    # retrieve any memory if it exists
    generation, matchboxes = load("matchboxes.json")
    # start the game
    game_running = True
    while game_running:
        # OTHERWISE TIE
        winner = winning_player(board_state)
        if len(open_tiles) == 0 and winner == NO_ONE:
            learn(winner, matchboxes, actions, open_tiles)
            clear()
            print("=====TIE=====")
            break

        # MENACE MOVES
        # show board state before
        show_board(generation, board_state)
        sleep(DELAY)
        # generate a matchbox if it doesn't exist for this board state
        if board_string(board_state) not in matchboxes:
            matchboxes.update({
                board_string(board_state): [*open_tiles]
            })
        # generate a random bead if a matchbox is empty
        if not matchboxes[board_string(board_state)]:
            matchboxes.update({
                board_string(board_state): [choice(open_tiles)]
            })
        # menace picks a bead from the matchbox for the current state
        # and action is recorded for later backpropogation
        if type(matchboxes[board_string(board_state)]) == int:
            bead = randint(0, 8)
        else:
            bead = choice(matchboxes[board_string(board_state)])
        actions.append((bead, board_string(board_state)))
        # remove from open_tiles
        open_tiles.remove(bead)
        # menace updates board state with its move
        board_state[bead] = MENACE
        # show decision
        show_board(generation, board_state)

        # CHECK IF MENACE WON
        winner = winning_player(board_state)
        if winner == MENACE:
            learn(winner, matchboxes, actions, open_tiles)
            clear()
            print("===== MENACE WINS =====")
            break
        # OTHERWISE TIE
        winner = winning_player(board_state)
        if len(open_tiles) == 0 and winner == NO_ONE:
            learn(winner, matchboxes, actions, open_tiles)
            clear()
            print("=====TIE=====")
            break


        # PLAYER MOVES
        # validate and retrieve player input
        # (must be int and in open_tiles)
        valid_input = False
        while not valid_input:
            # display board state after MENACE move before player move
            show_board(generation, board_state)
            try:
                X = int(input("""
                1|2|3
                -+-+-
                4|5|6
                -+-+-
                7|8|9
                """))
                X -= 1  # correct offset
            except:
                exit()
            if X not in open_tiles:
                continue
            else:
                valid_input = True
        # remove from open_tiles
        open_tiles.remove(X)
        # update board state with player move
        board_state[X] = PLAYER

        # CHECK IF MENACE LOST
        winner = winning_player(board_state)
        if winner == PLAYER:
            learn(winner, matchboxes, actions, open_tiles)
            clear()
            print("===== MENACE LOSES =====")
            break
        # OTHERWISE TIE
        winner = winning_player(board_state)
        if len(open_tiles) == 0 and winner == NO_ONE:
            learn(winner, matchboxes, actions, open_tiles)
            clear()
            print("=====TIE=====")
            break

    # store any learned info from the game
    save("matchboxes.json", generation + 1, matchboxes)


if __name__ == '__main__':
    main()
