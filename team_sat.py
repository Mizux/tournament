#!/usr/bin/env python3
"""Example of a simple player scheduling problem."""
import argparse
from ortools.sat.python import cp_model

def main():
    """Entry point of the program"""
    parser = argparse.ArgumentParser(description='Compute tournament schedule.')
    parser.add_argument('--players',
                        '-p',
                        default=12,
                        type=int,
                        help='number of players, must be even (default:12)')
    parser.add_argument('--turns',
                        '-t',
                        default=6,
                        type=int,
                        help='number of turns (max players / 2) (default:6)')
    args = vars(parser.parse_args())


    # Data.
    num_players = args['players']
    if num_players % 2 != 0:
        print(f"ERROR: num players must be even (here {num_players})")
        exit(2)

    num_turns = min(args['turns'], num_players // 2)

    num_games = args['players'] // 2
    print(f"players: {num_players}, turns: {num_turns}, games per turn: {num_games}")

    # Creates the model.
    model = cp_model.CpModel()

    # Creates games variables.
    all_players = range(num_players)
    all_turns = range(num_turns)
    all_games = range(num_games)
    # games[(p, t, g)]: player 'p' play on turn 't' the game 'g'.
    games = {}
    for player in all_players:
        for turn in all_turns:
            for game in all_games:
                games[(player, turn, game)] = model.NewBoolVar(f'p{player}_t{turn}_g{game}')

    # Each game is assigned to exactly two players.
    for turn in all_turns:
        for game in all_games:
            tmp_players = []
            for player in all_players:
                tmp_players.append(games[(player, turn, game)])
            model.Add(sum(tmp_players) == 2)

    # Each player plays one game per turn.
    for player in all_players:
        for turn in all_turns:
            model.AddExactlyOne(games[(player, turn, game)] for game in all_games)

    # Each player plays at most one the n-th game.
    for player in all_players:
        for game in all_games:
            model.AddAtMostOne(games[(player, turn, game)] for turn in all_turns)

    # Each player plays at most one game against other players.
    for p_1 in all_players:
        for p_2 in range(p_1+1, num_players):
            tmp = []
            for turn in all_turns:
                for game in all_games:
                    b_var = model.NewBoolVar(f'b_p{p_1}_p{p_2}_t{turn}_g{game}')
                    model.Add(games[(p_1, turn, game)] + games[(p_2, turn, game)] == 2).OnlyEnforceIf(b_var)
                    model.Add(games[(p_1, turn, game)] + games[(p_2, turn, game)] != 2).OnlyEnforceIf(b_var.Not())
                    tmp.append(b_var)
            model.AddAtMostOne(tmp)

    # [Optional] Force first turn to be in order 0 vs 1, 2 vs 3, 3 vs 4 ....
    #for player in all_players:
    #    model.Add(games[player, 0, player // 2] == 1)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 2
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True

    class PlayersPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
        """Print intermediate solutions."""
        def __init__(self, games, num_players, num_turns, num_games, limit):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self._games = games
            self._num_players = num_players
            self._num_turns = num_turns
            self._num_games = num_games
            self._solution_count = 0
            self._solution_limit = limit

        def on_solution_callback(self):
            """Print the current solution."""
            self._solution_count += 1
            print(f'Solution {self._solution_count}', ' '.join([f'game {i:03}' for i in range(num_games)]))
            for turn in range(self._num_turns):
                games = {}
                for game in range(self._num_games):
                    games[game] = []
                    for player in range(self._num_players):
                        if self.Value(self._games[(player, turn, game)]):
                            #print(f'  player {player} plays game {game}')
                            games[game].append(player)
                str_games = [f'  {v}' for v in games.values()]
                print(f' turn {turn}: ', ' '.join(str_games) )
            if self._solution_count >= self._solution_limit:
                print(f'Stop search after {self._solution_limit} solutions')
                self.StopSearch()

        def solution_count(self):
            """Return number of solution found so far."""
            return self._solution_count

    # Display the first five solutions.
    solution_limit = 3
    solution_printer = PlayersPartialSolutionPrinter(games, num_players,
                                                    num_turns, num_games,
                                                    solution_limit)

    # solve
    solver.Solve(model, solution_printer)

    # Statistics.
    print('\nSolver Statistics:')
    print(f'- conflicts      : {solver.NumConflicts()}')
    print(f'- branches       : {solver.NumBranches()}')
    print(f'- wall time      : {solver.WallTime()} s')
    print(f'- solutions found: {solution_printer.solution_count()}')


if __name__ == '__main__':
    main()
