from minesweeper import Game
import painter
import cv2

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

def open_cell():
    while True:
        a = input("open: ").upper()
        if len(a) != 3:
            print(f"index must be formattede as A00")
            continue
        try:
            r0 = "ABCDEFGHIJKLMNOPQ".find(a[0])
            r1 = int(a[1:3])
        except:
            print(f"index must be formattede as A00")
            continue
        if r0 == -1 or r1 < 0 or r1 > 29:
            print(f"no such cell {a}")
            continue
        return r0, r1

def test_a():
    game = Game((30, 17), 5)
    while not game.over:
        cv2.imwrite("image.png", painter.from_2d(game.get_field(), painter.maps.default))
        ans = game.open(*open_cell())
        if ans[0] != 1:
            print(ans[1])
    
    cv2.imwrite("image.png", painter.from_2d(game.get_field(), painter.maps.default))

def test_b():
    t = painter.parts.font[9:18, 40:45]
    print(t.shape)
    cv2.imwrite("image.png", t)

# print(open_cell())

test_a()