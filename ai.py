"""
Module for AI opponent.
"""

def move(game):
    """
    Move randomly for now.
    """
    move = win(game)
    if not move:
        move = block(game)
    if not move:
        move = fork(game)
    if not move:
        move = block_fork(game)
    if not move:
        move = random_move(game)
    (x, y) = move
    return game.move("ai", x, y)

#FIXME: DELETE ME
def random_move(game):
    """
    Move randomly.  Doesn't even check for valid moves.
    
    """
    import random
    move = (random.randrange(0, 3), random.randrange(0, 3))
    return move

def winning_move(game, player):
    """
    Look for a move that will win the game.  Take it, if one is found.

    """

    opponent = game.get_opponent(player)
    opponent_mark = game.get_mark(opponent)
    my_mark = game.get_mark(player)
    paths = game.traverse_board(banned=[opponent_mark], requires={my_mark: 2})

    for p in paths:
        for coords in p:
            if game.square_lookup(coords) == " ":
                print("Win condition for: %s" % player)
                return coords
    return False

def forking_move(game, player, format="single"):
    """
    Look for a move that will result in two possible ways to win,
    guaranteeing victory if the opposition can't win next round.

    """

    opponent = game.get_opponent(player)
    opponent_mark = game.get_mark(opponent)
    my_mark = game.get_mark(player)

    # Get a list of paths that have 1 move taken, unblocked by opponent.
    paths = game.traverse_board(banned=[opponent_mark], requires={my_mark: 1})

    # Pathways are irrelevent, make one list.
    coord_list = []
    for e in paths:
        for c in e:
            coord_list.append(c)

    print("coord_list: %s" % coord_list)

    # Intersect them, checking for overlapping coordinates.
    coords = {}
    for e in coord_list:
        if e not in coords.keys():
            # Because of the way traverse_board slices the board,
            # moves intersect with themselves, leading to strange math.
            # Delete them, compare only spaces from this point forward.
            if game.square_lookup(e) == my_mark:
                continue

            # We're tracking intersections, not numbers,
            # so start with 0.
            coords[e] = 0
        else:
            coords[e] += 1

    # Pick the most vicious fork possible.  I.e., most intersections.
    max = 0
    for e in coords.keys():
        max = coords[e] if coords[e] > max else max

    # If max is not > 0, then there aren't any interesting
    # intersections.
    return_list = []
    if max > 0:
        for e in coords.keys():
            if coords[e] == max:
                # We're indexing by coords, so just return e.
                if format == "single":
                    return e
                elif format == "list":
                    return_list.append(e)

    if format == "list":
        return return_list

    #FIXME: Why do you keep returning False?  Doesn't it make
    #FIXME: more sense to return None?  Look into it.
    return False

def list_forcing_moves(game, player):
    """
    Return moves that force opponent to move, thus preventing
    him from making a fork you can't block otherwise.

    """

    opponent = game.get_opponent(player)
    opponent_mark = game.get_mark(opponent)
    my_mark = game.get_mark(player)
    paths = game.traverse_board(banned=[opponent_mark], requires={my_mark: 1})

    coord_list = []
    move_list = []
    for e in paths:
        for c in e:
            coord_list.append(c)

    for e in coord_list:
        if game.square_lookup(e) != my_mark:
            move_list.append(e)

    return move_list

def win(game):
    """
    Win, if able.

    """
    move = winning_move(game, "ai")
    if move:
        print("FTW!")
    return move

def block(game):
    """
    Block opponent from winning, if able.

    """
    move = winning_move(game, game.get_opponent("ai"))
    if move:
        print("OH NO YOU DON'T!")
    return move

def fork(game):
    """
    Create a fork, resulting in multiple ways to win.

    """
    move = forking_move(game, "ai")
    if move:
        print("Fork!")
    return move

def block_fork(game):
    """
    Detect a fork, and block it.

    """
    move = None
    forks = forking_move(game, game.get_opponent("ai"), format="list")
    if len(forks) == 1:
        move = forks[0]
    else:
        print("Brute force!")
        force_moves = list_forcing_moves(game, "ai")
        from sets import Set
        fork_set = Set(forks)
        force_set = Set(force_moves)
        try:
            move = list(force_set - fork_set)[0]
        except IndexError:
            pass

    if move:
        print("A FISHFORK IS NO MATCH FOR MY MACHINE.")
    return move
