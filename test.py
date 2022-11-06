from minesweeper import Game
import painter

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

def test_game():
    game = Game((30, 17))

    while not game.over:
        print_field(game.get_field())
        x, y = map(int, input("open x y: ").split())
        print(game.open(y, x))

    print_field(game.get_field())

game = Game((30, 17))
game.open(10, 10)
painter.show_image(painter.from_2d(game.get_field(), painter.maps.default))