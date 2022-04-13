[![Python3 test](https://github.com/Mizux/tournament/actions/workflows/test.yml/badge.svg)](https://github.com/Mizux/tournament/actions/workflows/test.yml)

# Introduction

Small test for Lucas...

## Usage

```sh
./team_sat.py -h
usage: team_sat.py [-h] [--players PLAYERS] [--turns TURNS]

Compute tournament schedule.

options:
  -h, --help            show this help message and exit
  --players PLAYERS, -p PLAYERS
                        number of players, must be even (default:12)
  --turns TURNS, -t TURNS
                        number of turns (max: players / 2) (default:6)
```

## Sample

```sh
./team_sat.py
players: 12, turns: 6, games per turn: 6
Solution 1
             game  0  game  1  game  2  game  3  game  4  game  5
 Turn    0:   [1, 7]   [4, 5]   [0, 9]  [6, 10]  [2, 11]   [3, 8]
 Turn    1:   [0, 8]   [3, 7]   [2, 5]  [9, 11]  [4, 10]   [1, 6]
 Turn    2:   [5, 6]   [8, 9]  [1, 11]   [4, 7]   [0, 3]  [2, 10]
 Turn    3:  [9, 10]   [1, 2]   [4, 8]   [3, 5]   [6, 7]  [0, 11]
 Turn    4:   [2, 3]  [6, 11]  [7, 10]   [0, 1]   [5, 8]   [4, 9]
 Turn    5:  [4, 11]  [0, 10]   [3, 6]   [2, 8]   [1, 9]   [5, 7]
 Player  0: games:[0, 1, 2, 3, 4, 5] opponents:[1, 3, 8, 9, 10, 11]
 Player  1: games:[0, 1, 2, 3, 4, 5] opponents:[0, 2, 6, 7, 9, 11]
 Player  2: games:[0, 1, 2, 3, 4, 5] opponents:[1, 3, 5, 8, 10, 11]
 Player  3: games:[0, 1, 2, 3, 4, 5] opponents:[0, 2, 5, 6, 7, 8]
 Player  4: games:[0, 1, 2, 3, 4, 5] opponents:[5, 7, 8, 9, 10, 11]
 Player  5: games:[0, 1, 2, 3, 4, 5] opponents:[2, 3, 4, 6, 7, 8]
 Player  6: games:[0, 1, 2, 3, 4, 5] opponents:[1, 3, 5, 7, 10, 11]
 Player  7: games:[0, 1, 2, 3, 4, 5] opponents:[1, 3, 4, 5, 6, 10]
 Player  8: games:[0, 1, 2, 3, 4, 5] opponents:[0, 2, 3, 4, 5, 9]
 Player  9: games:[0, 1, 2, 3, 4, 5] opponents:[0, 1, 4, 8, 10, 11]
 Player 10: games:[0, 1, 2, 3, 4, 5] opponents:[0, 2, 4, 6, 7, 9]
 Player 11: games:[0, 1, 2, 3, 4, 5] opponents:[0, 1, 2, 4, 6, 9]
```
