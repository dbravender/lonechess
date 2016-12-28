from collections import namedtuple
from copy import deepcopy


def until_a_piece_is_hit(x, y, xoff, yoff, occupied_spots):
    while x >= 0 and y >= 0 and x <= 4 and y <= 4:
        x += xoff
        y += yoff
        if (x, y) in occupied_spots:
            yield x, y
            break


class Pawn:
    symbol = '♟'

    @staticmethod
    def moves(x, y, occupied_spots):
        yield x - 1, y + 1
        yield x - 1, y - 1


class King:
    symbol = '♚'

    @staticmethod
    def moves(x, y, occupied_spots):
        for xoff in [-1, 0, 1]:
            for yoff in [-1, 0, 1]:
                if xoff == 0 and yoff == 0:
                    continue
                if (x + xoff, y + yoff) in occupied_spots:
                    yield x + xoff, y + yoff


class Bishop:
    symbol = '♝'

    @staticmethod
    def moves(x, y, occupied_spots):
        for xoff, yoff in [(-1, -1), (1, 1), (-1, 1), (1, -1)]:
            for location in until_a_piece_is_hit(x, y, xoff, yoff,
                                                 occupied_spots):
                yield location


class Rook:
    symbol = '♜'

    @staticmethod
    def moves(x, y, occupied_spots):
        for xoff, yoff in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            for location in until_a_piece_is_hit(x, y, xoff, yoff,
                                                 occupied_spots):
                yield location


class Queen:
    symbol = '♛'

    @staticmethod
    def moves(x, y, occupied_spots):
        for move in Bishop.moves(x, y, occupied_spots):
            yield move
        for move in Rook.moves(x, y, occupied_spots):
            yield move


class Knight:
    symbol = '♞'

    @staticmethod
    def moves(x, y, occupied_spots):
        for xoff, yoff in [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                           (1, -2), (1, 2), (2, -1), (2, 1)]:
            yield x + xoff, y + yoff


class LoneChess(object):
    """Chess puzzles"""
    State = namedtuple('LoneChessState', ['pieces', 'history'])
    Move = namedtuple('Move', ['from_x', 'from_y', 'to_x', 'to_y'])

    @classmethod
    def initial_state(cls, pieces):
        return cls.State(pieces=pieces, history=[])

    @classmethod
    def apply_move(cls, state, move):
        # copy all pieces
        pieces = deepcopy(state.pieces)
        history = state.history[:]
        moving_piece = pieces[(move.from_x, move.from_y)]
        del pieces[(move.from_x, move.from_y)]
        pieces[(move.to_x, move.to_y)] = moving_piece
        history.append(pieces)
        if not len(state.pieces) == len(pieces) + 1:
            assert False
        return state._replace(pieces=pieces, history=history)

    @classmethod
    def get_moves(cls, state):
        moves = []
        for location, piece in state.pieces.items():
            x, y = location
            potential_moves = list(piece.moves(x, y, state.pieces))
            valid_moves = [(to_x, to_y) for to_x, to_y in potential_moves
                           if (to_x, to_y) in state.pieces]
            moves.extend([cls.Move(from_x=x, from_y=y, to_x=to_x, to_y=to_y)
                          for to_x, to_y in valid_moves])
        return moves

    @staticmethod
    def end(state):
        return len(state.moves) == 0

    @staticmethod
    def print_board(board):
        print('-' * 4)
        for x in range(4):
            for y in range(4):
                try:
                    print(board[(x, y)].symbol, end='')
                except KeyError:
                    print('.', end='')
            print('')


def get_children(node):
    return [LoneChess.apply_move(node, move)
            for move in LoneChess.get_moves(node)]


def get_solutions(initial_state):
    current_nodes = [initial_state]
    next_nodes = []
    winners = []
    total_nodes = 0

    while current_nodes:
        total_nodes += len(current_nodes)
        for node in current_nodes:
            new_children = get_children(node)
            winners.extend([child for child in new_children
                            if len(child.pieces) == 1])
            if (len(winners) > 1 and
                    not all([w.pieces == winners[0].pieces for w in winners])):
                return winners
            next_nodes.extend(new_children)
        current_nodes = next_nodes
        next_nodes = []

    if winners:
        if all([w.pieces == winners[0].pieces for w in winners]):
            return [winners[0]]
    return winners


lone_chess = LoneChess.initial_state(pieces={(0, 0): Knight,
                                             (0, 1): Rook,
                                             (1, 1): King,
                                             (1, 3): Knight,
                                             (2, 0): Pawn,
                                             (2, 2): Bishop})

LoneChess.print_board(lone_chess.pieces)
for state in get_solutions(lone_chess)[0].history:
    LoneChess.print_board(state)
