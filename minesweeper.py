from random import sample

class Cell:
    def __init__(self, mine: bool, opened: int) -> None:
        if mine:
            print("1", end="")
        self.mine = mine
        self.opened = opened # -1 closed, 0 no mines, 1-8 there is mines, 9 it is mine, 10 blown, 11 marked

class Game:
    field: list[list[Cell]]
    moves: int
    over: bool
    victory: bool
    
    def __init__(self, size: tuple[int, int], mines: int = 50) -> None:
        w, h = size
        samp = sample(range(w*h),k=mines)
        self.field = [[Cell(x+w*y in samp, -1) for x in range(w)] for y in range(h)]
        self.moves = 0
        self.over = False
        self.victory = False
    
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
        
    def open(self, x, y, move=True):
        if self.field[x][y].opened != -1:
            return -1, f"Cell {x,y} already opened"
        if self.field[x][y].mine:
            self.over = True
            self.field[x][y].opened = 10
            return 0, f"Game over! There was mine"
        s = 0
        for tx in (-1,0,1):
            for ty in (-1,0,1):
                s += self._is_mine(x+tx,y+ty)
        
        self.field[x][y].opened = s
        self.moves += 1
        
        lx, ly = len(self.field), len(self.field[0])
        if s == 0:
            for tx in (-1,0,1):
                for ty in (-1,0,1):
                    dx, dy = x+tx, y+ty
                    if all((dx>=0, dy>=0, dx<lx, dy<ly)):
                        self.open(dx, dy, move=False)

        if move:
            s = 0
            for row in self.field:
                for c in row:
                    if c.mine or c.opened != -1:
                        s += 1
            if s == lx*ly:
                self.over = True
                self.victory = True
                return 0, f"Game over! You won!"
                
        return 1, f"Game continues"
        