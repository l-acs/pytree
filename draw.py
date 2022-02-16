from PIL import Image, ImageDraw, ImageFont
from pprint import pprint

# import shlex
import sys
# from enum import Enum

font_size = 32
font = ImageFont.truetype('FreeMono.ttf', font_size)
margin = 50
fill_color = (0, 0, 0)

thickness = 3

# how many pixels should vertically separate a node and its immediate children?
line_height = 30




class TextDraw:
    def __init__ (self, text):
        self.text = text
        W = 10000
        H = 10000

        i = Image.new("RGBA",(W,H),"white") # random
        d = ImageDraw.Draw(i)

        (w, h) = d.textsize(text)

        self.size = (w, h)


    def display (self):
        pprint(self.text)
        pprint(self.size)
    



class Test:
    def TextDraw ():
        h = "Hello"
        td = TextDraw(h)
        td.display()

        lines = ["Yes", "Indeed", "This is a big long sentence which is very big and which is also very long"]

        for line in lines:
            TextDraw(line).display()

        TextDraw('\n'.join(lines)).display()


def main() -> int:
    Test.TextDraw()
    return 0



if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
