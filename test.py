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
            
game = Game((5, 5))

print(game.open(2, 2))

# game.over = True
print_field(game.get_field())