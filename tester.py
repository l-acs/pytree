from pprint import pprint
# import shlex
import sys

from PIL import Image, ImageDraw, ImageFont
from draw import TextDraw, LineDraw



class Test:
    def TextDrawMath ():
        h = "Hello"
        td = TextDraw(h)
        td.display()
        print(20 * '---')

        lines = ["Yes", "Indeed", "This is a big long sentence which is very big and which is also very long"]

        coord = (100, 50)


        W, H = 1000, 1000
        i = Image.new("RGBA",(W,H),"white") # random



        for line in lines:
            td = TextDraw(line)
            td.display()
            print('Coord:')
            print(coord)
            print('Top left:')
            print(td.get_top_left(coord))
            print('Below:')
            print(td.get_coord_below(coord))

            print('After drawing:')
            pprint(td.draw(i, coord))
            print(20 * '---')
            

        TextDraw('\n'.join(lines))

    def TextDrawMultiline (image, coord):
        lines = ["Yes", "Indeed", "This is a big long sentence which is very big and which is also very long"]
        
        s = '\n'.join(lines)

        td = TextDraw(s)
        new_coord = td.draw(image, coord)
        pprint(new_coord)
        return new_coord

    def TextDrawSeparateLines (image, coord):
        lines = ["Yes", "Indeed", "This is a big long sentence which is very big and which is also very long"]
        
        # s = '\n'.join(lines)

        for line in lines:
            td = TextDraw(line)
            coord = td.draw(image, coord)
            pprint(coord)

        return coord


    def LineDrawMath ():
        print("hey")
        coord = (100, 50)


        W, H = 1000, 1000
        i = Image.new("RGBA",(W,H),"white") # random

        delta_x, delta_y = (50, 100)


        line = LineDraw(coord, delta_x, delta_y)

        line.display()


def main() -> int:
    W, H = 2500, 1000
    i = Image.new("RGBA",(W,H),"white") # random


    Test.TextDrawMath()
    coord = (W/2, 50)
    coord = Test.TextDrawMultiline(i, coord)
    # i.show()

    # coord = (W/2, 500)
    Test.TextDrawSeparateLines(i, coord)
    i.show()


    Test.LineDrawMath()

    return 0



if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
