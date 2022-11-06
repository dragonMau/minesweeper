import numpy as np
import cv2

home = "."


def show_image(im, name='image'):
    cv2.imshow(name, im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

class parts:
    default = np.zeros((32,32,3), np.uint8)
    cell = cv2.imread(f'{home}/assets/cell.png')
    cell0 = cv2.imread(f'{home}/assets/cell0.png')
    
    
class maps:
    @staticmethod
    def default(cell, x, y):
        if cell == -1:
            return parts.cell
        if cell == 0:
            return parts.cell0
        else:
            return parts.default

def from_2d(l2d: list[list[int]], map):
    h = len(l2d)
    w = len(l2d[0])
    blank = np.zeros((h*32,w*32,3), np.uint8)
    for y, row in enumerate(l2d):
        for x, cell in enumerate(row):
            blank[y*32:(y+1)*32, x*32:(x+1)*32] = map(cell, x, y)
    return blank