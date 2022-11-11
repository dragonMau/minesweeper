import numpy as np
import cv2

home = "d://Users/mseli/progs/minesweeper"

def show_image(im, name='image'):
    cv2.imshow(name, im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

class parts:
    font = cv2.imread(f'{home}/assets/font.png')
    cell = cv2.imread(f'{home}/assets/cell.png')
    cell0 = cv2.imread(f'{home}/assets/cell0.png')
    cell1 = cv2.imread(f'{home}/assets/cell1.png')
    cell2 = cv2.imread(f'{home}/assets/cell2.png')
    cell3 = cv2.imread(f'{home}/assets/cell3.png')
    cell4 = cv2.imread(f'{home}/assets/cell4.png')
    cell5 = cv2.imread(f'{home}/assets/cell5.png')
    cell6 = cv2.imread(f'{home}/assets/cell6.png')
    cell7 = cv2.imread(f'{home}/assets/cell7.png')
    cell8 = cv2.imread(f'{home}/assets/cell8.png')
    cellB = cv2.imread(f'{home}/assets/cellB.png')
    cellE = cv2.imread(f'{home}/assets/cellE.png')
    cellM = cv2.imread(f'{home}/assets/cellM.png')
    default = np.zeros((32,32,3), np.uint8)

font_dict = {"A": (0,   0), "J": (0,  9), "1": (0,  18),
             "B": (5,   0), "K": (5,  9), "2": (5,  18),
             "C": (10,  0), "L": (10, 9), "3": (10, 18),
             "D": (15,  0), "M": (15, 9), "4": (15, 18),
             "E": (20,  0), "N": (20, 9), "5": (20, 18),
             "F": (25,  0), "O": (25, 9), "6": (25, 18),
             "G": (30,  0), "P": (30, 9), "7": (30, 18),
             "H": (35,  0), "Q": (35, 9), "8": (35, 18),
             "I": (40,  0), "0": (40, 9), "9": (40, 18)}
    
class maps:
    @staticmethod
    def default(cell, x, y):
        match cell:
            case -1:
                temp = parts.cell
                text = f"{'ABCDEFGHIJKLMNOPQ'[y]}{x:02d}"
                
                lx, ly = font_dict[text[0]]
                temp[11:20,  6:11] = parts.font[ly:ly+9, lx:lx+5]
                
                lx, ly = font_dict[text[1]]
                temp[11:20, 13:18] = parts.font[ly:ly+9, lx:lx+5]
                
                lx, ly = font_dict[text[2]]
                temp[11:20, 20:25] = parts.font[ly:ly+9, lx:lx+5]
                
                return temp
            case  0: return parts.cell0
            case  1: return parts.cell1
            case  2: return parts.cell2
            case  3: return parts.cell3
            case  4: return parts.cell4
            case  5: return parts.cell5
            case  6: return parts.cell6
            case  7: return parts.cell7
            case  8: return parts.cell8
            case  9: return parts.cellB
            case 10: return parts.cellE
            case 11: return parts.cellM
            case  _: return parts.default

def from_2d(l2d: list[list[int]], map_):
    h = len(l2d)
    w = len(l2d[0])
    blank = np.zeros((h*32,w*32,3), np.uint8)
    for y, row in enumerate(l2d):
        for x, cell in enumerate(row):      
            blank[y*32:(y+1)*32, x*32:(x+1)*32] = map_(cell, x, y)
    return blank
