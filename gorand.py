#!/usr/bin/env python3

import sys
import subprocess
import tempfile
import argparse
import random
import os

def get_args():
    parser = argparse.ArgumentParser("start a randomized Go position in GNU Go")
    parser.add_argument("-b", "--boardsize", help = "Board size (default = 19).", default=19, type = int)
    parser.add_argument("-H", "--handicap", help = "Handicap (default = 0).", default=0, type = int)
    parser.add_argument("-r", "--random_moves", help = "Number of random moves (default = 0).", default=0, type = int)
    parser.add_argument("-R", "--run_gnugo", help = "Flag to run game directly in gnugo, rather than printing .sgf file to stdout (default = False).", default = False, action = "store_true")
    parser.add_argument("-g", "--gnugo_options", help = "Options to pass to GNU Go.", default=None)
    parser.add_argument("-s", "--symmetric", help = "Make random moves rotationally symmetric between black and white", action = "store_true")
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

def symmetric_move(boardsize, color, mirror_move):
    new_xcoord = boardsize - mirror_move[1] - 1
    new_ycoord = boardsize - mirror_move[2] - 1
    return((color, new_xcoord, new_ycoord))

def generate_sym_move_pair(boardsize):
    move1 = generate_move(boardsize, "black")
    move2 = symmetric_move(boardsize, "white", move1)
    return((move1, move2))

def unique_move(move, moves_list):
    ok = True
    for old_move in moves_list:
        if move[1] == old_move[1] and move[2] == old_move[2]:
            ok = False
    return(ok)

def generate_moves(boardsize = 19, handicap = 0, random_moves = 0, symmetric = False):
    moves_list = []
    
    handicap_moves_to_generate = handicap
    while(handicap_moves_to_generate > 0):
        new_move = generate_move(boardsize, "black")
        if unique_move(new_move, moves_list):
            moves_list.append(new_move)
            handicap_moves_to_generate -= 1
        
    random_moves_to_generate = random_moves
    while(random_moves_to_generate > 0):
        if symmetric:
            new_move_pair = generate_sym_move_pair(boardsize)
        else:
            new_move_pair = generate_move_pair(boardsize)
        if unique_move(new_move_pair[0], moves_list) and unique_move(new_move_pair[1], moves_list):
            moves_list.append(new_move_pair[0])
            moves_list.append(new_move_pair[1])
            random_moves_to_generate -= 1
    return(moves_list)

def generate_moves_from_args(args):
    return generate_moves(boardsize = args.boardsize, handicap = args.handicap, random_moves = args.random_moves, symmetric = args.symmetric)

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

def moves2sgf(moves, size):
    out = ["(;"]
    out.extend(["SZ[", str(size), "];"])
    for move in moves:
        out.append(move2sgf(move))
    out.append(")")
    return("".join(out))

def run_gnugo(sgf, options):
    sgf_file = tempfile.NamedTemporaryFile(delete=False, mode = "w")
    sgf_path = sgf_file.name
    sgf_file.write(sgf)
    sgf_file.close()
    command = ["gnugo", "-l", sgf_path, "--mode", "ascii"]
    if options: command.extend(options.split())
    
    subprocess.run(command)
    
    os.remove(sgf_path)

def main():
    args = get_args()
    moves = generate_moves_from_args(args)
    sgf = moves2sgf(moves, args.boardsize)
    if args.run_gnugo:
        run_gnugo(sgf, args.gnugo_options)
    else:
        print(sgf)

if __name__ == "__main__":
    main()
