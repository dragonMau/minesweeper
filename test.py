from minesweeper import Game

def print_field(field):
    for line in field:
        cl = []
        for c in line:
            cl.append(
                "X" if c == 9 else\
                "—" if c == -1 else\
                c
            )
        print(*cl)
            
game = Game((10, 30))

while not game.over:
    print_field(game.get_field())
    x, y = map(int, input("open x y: ").split())
    print(game.open(y, x))

print_field(game.get_field())