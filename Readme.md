# Go Rand

A random start generator for the game of Go.

## Introduction

When a game like Go is always played from an empty board, opening theory can
begin to dominate the game, and the entire opening can become an exercise in
memorization. Go Rand generates a randomized start where several pieces are
already on the board. If you use the `-s` option, the plays are rotationally
symmetric for black and white, so they should be _relatively_ balanced.

## Usage

```sh
gorand [-h] [-b BOARDSIZE] [-H HANDICAP] [-r RANDOM_MOVES] [-R] [-g GNUGO_OPTIONS]
```

To generate a 19x19 board with three random, paired plays:

```sh
gorand -b 19 -r 3 -s
```

## Installation

Simply copy `gorand.py` to any directory that's in your PATH, and rename it `gorand`.

## Dependencies

Optional: GNU Go, if you want to use the `-R` option.
