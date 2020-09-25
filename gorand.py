#!/usr/bin/env python3

import sys
import subprocess
import tempfile
import argparse
import random

def get_args():
    parser = argparse.ArgumentParser("start a randomized Go position in GNU Go")
    parser.add_argument("-b", "--boardsize", help = "Board size (default = 19).", default=19, type = int)
    parser.add_argument("-H", "--handicap", help = "Handicap (default = 0).", default=0, type = int)
    parser.add_argument("-r", "--random_moves", help = "Number of random moves (default = 0).", default=0, type = int)
    args = parser.parse_args()
    return(args)

def generate_move(boardsize, color):
    xcoord = random.randrange(0, boardsize)
    ycoord = random.randrange(0, boardsize)
    return((color, xcoord, ycoord))

def generate_move_pair(boardsize):
    move1 = generate_move(boardsize, "black")
    move2 = generate_move(boardsize, "white")
    return((move1, move2))

def unique_move(move, moves_list):
    ok = True
    for old_move in moves_list:
        if move[1] == old_move[1] and move[2] == old_move[2]:
            ok = False
    return(ok)

def generate_moves(args):
    moves_list = []
    
    handicap_moves_to_generate = args.handicap
    while(handicap_moves_to_generate > 0):
        new_move = generate_move(args.boardsize, "black")
        if unique_move(new_move, moves_list):
            moves_list.append(new_move)
            handicap_moves_to_generate -= 1
        
    random_moves_to_generate = args.random_moves
    while(random_moves_to_generate > 0):
        new_move_pair = generate_move_pair(args.boardsize)
        if unique_move(new_move_pair[0], moves_list) and unique_move(new_move_pair[1], moves_list):
            moves_list.append(new_move_pair[0])
            moves_list.append(new_move_pair[1])
            random_moves_to_generate -= 1
    return(moves_list)

def move2sgf(move):
    positions = "abcdefghijklmnopqrstuvwxyz"
    colors = {"black": "B", "white": "W"}
    out = (
        colors[move[0]],
        positions[move[1]],
        positions[move[2]]
    )
    outstring = "A%s[%s%s]" % out
    return(outstring)

def moves2sgf(moves):
    out = ["(;"]
    for move in moves:
        out.append(move2sgf(move))
    out.append(")")
    return("".join(out))

def main():
    args = get_args()
    moves = generate_moves(args)
    sgf = moves2sgf(moves)
    print(args)
    print(moves)
    print(sgf)
    # run_gnugo(sgf)

if __name__ == "__main__":
    main()
