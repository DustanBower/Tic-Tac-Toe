#!/usr/bin/env python2

"""
Game logic code module.
"""

from __future__ import print_function

class Game:
    # List of functions to call when we update the board.
    updates = []
    main_loop = None
    winner = None

    def __init__(self, gui=None):
        import random
        self.board = {}
        for x in range(0, 3):
            self.board[x] = {}
            for y in range(0, 3):
                self.board[x][y] = " "

        self.turn = random.choice(["human", "ai"])
        print("%s's turn." % self.turn)
        self.check_ai_move()

    def move(self, player, x, y):
        mark = self.get_mark(player)
        if self.board[x][y] == " ":
            self.board[x][y] = mark
            self.send_update()
            self.next_turn()
            return True
        return False

    def get_mark(self, player):
        return "X" if player == "human" else "O"

    def get_board(self):
        return self.board

    def next_turn(self):
        if not self.turn:
            return
        old = self.turn
        self.turn = "ai" if self.turn != "ai" else "human"
        print("Was %s's turn, now %s's." % (old, self.turn))
        self.check_ai_move()

    def check_ai_move(self):
        if self.turn == "ai":
            import ai
            valid_move = False
            while not valid_move:
                valid_move = ai.move(self)
            self.send_update()

    def check_for_win(self):
        winner = None

        paths = self.traverse_board()

        # e represents a pathway.  That is, a list of 3 coordinates that make
        # a potentially valid tic-tac-toe row.  Passing these to square lookup
        # converts them into self.board[x][y] without causing eyebleeding.
        for e in paths:
            if((self.square_lookup(e[0])
                == self.square_lookup(e[1])
                == self.square_lookup(e[2]))
               and self.square_lookup(e[0]) != " "):
                winner = self.square_lookup(e[0])
                break

        if winner:
            self.turn = None
            print("Winner: %s" % winner)

    def square_lookup(self, coords):
        return self.board[coords[0]][coords[1]]

    def ascii_board(self):
        for x in range(0, 3):
            print("\n----------")
            for y in range(0, 3):
                print("|" + self.board[x][y] + "|", end="")

        print("\n----------")

    def register_update(self, what, *args):
        print("register_update: %s" % what)
        d = {}
        d['function'] = what
        d['args'] = args
        print("register_update: %s" % repr(d))
        self.updates.append(d)

    def send_update(self):
        self.ascii_board()
        print(self.updates)
        for e in self.updates:
            e['function'](*e['args'])

    # Calling gtk.main from here breaks encapsulation,
    # so let's wrap it with these functions.
    def register_main_loop(self, what, *args):
        self.main_loop = {}
        self.main_loop['function'] = what
        self.main_loop['args'] = args

    def enter_main_loop(self):
        self.main_loop['function'](*self.main_loop['args'])

    def traverse_board(self):
        """
        Traverse the board and return the eight different pathways
        as a list of lists.
        """
        paths = []
        # rows
        for row in range(0, 3):
            pathway = []
            for col in range(0, 3):
                pathway.append((row, col))
            paths.append(pathway)

        # columns
        for col in range(0, 3):
            pathway = []
            for row in range(0, 3):
                pathway.append((row, col))
            paths.append(pathway)

        # diagonals
        pathway = []
        for row in range(0, 3):
            col = row  # diagonal magic
            pathway.append((row, col))
        paths.append(pathway)

        pathway = []
        # Need to reverse the diagonal.  Subtracting
        # 2 and taking the absolute value yields the
        # appropriate numbers.
        for row in (range(0, 3)):
            col = abs(row-2)
            pathway.append((row, col))
        paths.append(pathway)

        return paths

if __name__ == "__main__":
    import gui
    game = Game()
    ui = gui.GUI(game)
    game.gui = ui
    # This needs to be at the end.  Perhaps a priority system
    # is in order here.
    game.register_update(game.check_for_win)
    game.send_update()
    game.enter_main_loop()
