import random
import sys
from enum import Enum
from abc import ABC, abstractmethod
import typing as tp


class Cell(Enum):
    E = 0
    X = 1
    O = 2


class Result(Enum):
    Unknown = 0
    Pair = 1
    Win = 2
    Lose = 3


class Move:
    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

class Position:
    def __init__(self, board: list[list[Cell]]):
        self.__board = board
        self.__n = len(board)

    @property
    def board(self):
        return self.__board

    @property
    def n(self):
        return self.__n

    def is_valid(self, move: Move) -> bool:
        return 0 <= move.x < self.n and 0 <= move.y < self.n and self.board[move.x][move.y] is Cell.E

class Player(ABC):
    def __init__(self, name: str = ''):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return self.name

    @abstractmethod
    def get_move(self, position: Position) -> Move:
        return Move(1, 1)

class RandomPlayer(Player):

    def __init__(self, name: str, seed: int | None = None):
        Player.__init__(self, name)
        self.seed = seed

    def get_move(self, position: Position) -> Move:
        if self.seed:
            random.seed(self.seed)
        x = random.randint(0, position.n - 1)
        y = random.randint(0, position.n - 1)
        move = Move(x, y)
        while not position.is_valid(move):
            x = random.randint(0, position.n - 1)
            y = random.randint(0, position.n - 1)
            move = Move(x, y)
        return move

class HumanPlayer(Player):
    def get_move(self, position: Position) -> Move:
        data = input().split()
        x = int(data[0])
        y = int(data[1])
        move = Move(x, y)
        while not position.is_valid(move):
            data = input().split()
            x = int(data[0])
            y = int(data[1])
            move = Move(x, y)
        return move


class OutUI(ABC):
    @abstractmethod
    def print(self, data: tp.Any) -> bool:
        pass

class ConsoleOutUI(OutUI):
    def __init__(self, out=sys.stdout):
        self.__out = out

    @property
    def out(self):
        return self.__out

    def print(self, data: tp.Any):
        print(data, file=self.out)

class TwoPlayerGame(ABC):
    @abstractmethod
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2

class TickTackToe(TwoPlayerGame):
    def __init__(self, n: int, player1: Player, player2: Player, out_ui: OutUI = ConsoleOutUI()):
        TwoPlayerGame.__init__(self, player1, player2)
        self.__n = n
        self.__out_ui = out_ui
        self.__board = Board(n)
        self.cur_player = player1
        self.cur_cell = Cell.X

    @property
    def n(self):
        return self.__n

    @property
    def out_ui(self):
        return self.__out_ui

    @property
    def board(self):
        return self.__board

    def change_player(self):
        if self.cur_player is self.player1:
            self.cur_player = self.player2
            self.cur_cell = Cell.O
        else:
            self.cur_player = self.player1
            self.cur_cell = Cell.X

    def start_game(self):
        state = self.board.check_state()
        while state is Result.Unknown:
            self.out_ui.print(f'Player {self.cur_player.name} makes play \n')
            move = self.cur_player.get_move(Position(self.board.cells))
            self.board.set_cell(move, self.cur_cell)
            self.out_ui.print(self.board)
            self.change_player()
            state = self.board.check_state()
        self.change_player()
        if state is Result.Pair:
            self.out_ui.print('Nobody wins')
        else:
            self.out_ui.print(f'Player {self.cur_player.name} win')

class TickTackToeWithMaxCells(TickTackToe):
    def __init__(self, n: int, l: int, player1: Player, player2: Player, out_ui: OutUI = ConsoleOutUI()):
        TickTackToe.__init__(self, n, player1, player2, out_ui)
        self.__l = l
        self.__player1_list: list[Move] = []
        self.__player2_list: list[Move] = []
        self.cur_player_list: list[Move] = []

    @property
    def l(self):
        return self.__l

    @property
    def player1_list(self):
        return self.__player1_list

    @property
    def player2_list(self):
        return self.__player2_list

    def change_player(self):
        if self.cur_player is self.player1:
            self.cur_player = self.player2
            self.cur_cell = Cell.O
            self.cur_player_list = self.player2_list
        else:
            self.cur_player = self.player1
            self.cur_cell = Cell.X
            self.cur_player_list = self.player1_list

    def start_game(self):
        state = self.board.check_state()
        while state is Result.Unknown:
            self.out_ui.print(f'Player {self.cur_player.name} makes play \n')
            move = self.cur_player.get_move(Position(self.board.cells))
            self.board.set_cell(move, self.cur_cell)
            self.cur_player_list.append(move)
            if len(self.cur_player_list) >= self.l:
                self.board.set_cell(self.cur_player_list.pop(0), Cell.E)
            self.out_ui.print(self.board)
            self.change_player()
            state = self.board.check_state()
        self.change_player()
        if state is Result.Pair:
            self.out_ui.print('Nobody wins')
        else:
            self.out_ui.print(f'Player {self.cur_player.name} win')

class Board:
    def __init__(self, n: int):
        self.n = n
        self.cells: list[list[Cell]] = [[Cell(0) for i in range(self.n)] for j in range(self.n)]

    @classmethod
    def eq_on_row(cls, row: tp.Iterable[Cell]) -> bool:
        last: Cell | None = None
        for e in row:
            if last is not None and last is not e:
                return False
            last = e
        return True

    def check_state(self) -> Result:
        empty = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.cells[i][j] is Cell.E:
                    empty += 1
        if empty == 0:
            return Result.Pair
        if self.eq_on_row([self.cells[i][i] for i in range(self.n)]) and self.cells[0][0] is not Cell.E:
            return Result.Win
        if self.eq_on_row([self.cells[self.n - i - 1][i] for i in range(self.n)]) and self.cells[self.n - 1][0] is not Cell.E:
            return Result.Win
        for i in range(self.n):
            if self.eq_on_row(self.cells[i]) and self.cells[i][0] is not Cell.E:
                return Result.Win
            if self.eq_on_row([self.cells[j][i] for j in range(self.n)]) and self.cells[0][i] is not Cell.E:
                return Result.Win
        return Result.Unknown

    def set_cell(self, move: Move, cell: Cell):
        self.cells[move.x][move.y] = cell

    def __str__(self):
        text = '* '
        for i in range(self.n):
            text += f'{i + 1} '
        text += '\n'
        for i in range(self.n):
            text += f'{i + 1} '
            for j in range(self.n):
                if self.cells[i][j] is Cell.E:
                    text += '* '
                elif self.cells[i][j] is Cell.X:
                    text += 'X '
                else:
                    text += 'O '
            text += '\n'
        return text


pl1 = RandomPlayer("1")
pl2 = RandomPlayer("2")

game = TickTackToeWithMaxCells(3, 4, pl1, pl2)
game.start_game()
