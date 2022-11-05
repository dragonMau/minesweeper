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
        self.field = [[Cell(random()<1/4.85, -1)\
            for _ in range(size[1])] for _ in range(size[0])]
        self.moves = 0
        self.over = False
    
    def get_field(self):
        return [[9 if cell.mine and self.over else cell.opened\
            for cell in line] for line in self.field]
    
    def _is_mine(self, x, y):
        lx, ly = len(self.field), len(self.field[0])
        if all((x>=0, y>=0, x<lx, y<ly)):
            return self.field[x][y].mine
        else:
            # print("OutOfBounds")
            return False
        
    def open(self, x, y):
        if self.field[x][y].opened != -1:
            return -1, f"Cell {x,y} already opened"
        if self.field[x][y].mine:
            self.over = True
            self.field[x][y].opened = 9
            return 0, f"Game over! There was mine"
        s = 0
        for tx in (-1,0,1):
            for ty in (-1,0,1):
                s += self._is_mine(x+tx,y+ty)
        
        self.field[x][y].opened = s
        self.moves += 1
        if s != 0: return 1, f"Game continues"
    
        for tx in (-1,0,1):
            for ty in (-1,0,1):
                dx, dy = x+tx, y+ty
                lx, ly = len(self.field), len(self.field[0])
                if all((dx>=0, dy>=0, dx<lx, dy<ly)):
                    self.open(dx, dy)
        