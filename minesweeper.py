from random import random

class Cell:
    def __init__(self, mine: bool, opened: int) -> None:
        self.mine = mine
        self.opened = opened # -1 closed, 0 no mines, 1-8 there is mines, 9 it is mine

class Game:
    field: list[list[Cell]]
    moves: int
    over: bool
    
    def __init__(self, size: tuple[int, int]) -> None:
        self.field = [[Cell(random()<1/4.85, -1) for _ in range(size[1])] for _ in range(size[0])]
        self.moves = 0
        self.over = False
    
    def get_field(self):
        r_field = [[0]*len(self.field[0])]*len(self.field)
        for x, line in enumerate(self.field):
            for y, cell in enumerate(line):
                r_field[x][y] = cell.opened
                if cell.mine and self.over:
                    r_field[x][y] = 9
        return r_field
    
    def _is_mine(self, x, y):
        if x < 0 or y < 0:
            return False
        try:
            return self.field[x][y].mine
        except IndexError:
            return False
        
    def open(self, x, y):
        if self.field[x][y].opened != -1:
            return -1, f"Cell {x,y} already opened"
        if self.field[x][y].mine:
            self.over = True
            return 0, f"Game over! There was mine"
        s = 0
        for tx in (-1,0,1):
            for ty in (-1,0,1):
                s += self._is_mine(x-tx,y-ty)
        self.field[x][y].opened = s
        return s