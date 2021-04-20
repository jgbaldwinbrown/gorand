#!/usr/bin/env python3

import gorand
import os

def main():
    outdir = "test_out/"
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    for i in range(100):
        out_path = outdir + ("game_%03d" % i)
        with open(out_path, "w") as outconn:
            game = gorand.generate_moves(symmetric = True, random_moves = 5, handicap = 9)
            sgf = gorand.moves2sgf(game, 19)
            outconn.write(sgf + "\n")

if __name__ == "__main__":
    main()
