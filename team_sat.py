#!/usr/bin/env python3
"""Example of a simple player scheduling problem."""
from ortools.sat.python import cp_model

def main(n):
    # Data.
    num_players = 2 * n
    num_turns = n
    num_games = n
    all_players = range(num_players)
    all_turns = range(num_turns)
    all_games = range(num_games)

    # Creates the model.
    model = cp_model.CpModel()

    # Creates games variables.
    # games[(t, r, g)]: player 't' play on turn 'r' the game 'g'.
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
            model.AddExactlyOne(games[(player, turn, game)] for turn in all_turns)

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
            print(f'Solution {self._solution_count}')
            for turn in range(self._num_turns):
                print(f' turn {turn}')
                for game in range(self._num_games):
                    for player in range(self._num_players):
                        if self.Value(self._games[(player, turn, game)]):
                            print(f'  player {player} plays game {game}')
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
    print('\nStatistics:')
    print(f'- conflicts      : {solver.NumConflicts()}')
    print(f'- branches       : {solver.NumBranches()}')
    print(f'- wall time      : {solver.WallTime()} s')
    print(f'- solutions found: {solution_printer.solution_count()}')


if __name__ == '__main__':
    main(n=4)
