from PIL import Image, ImageDraw, ImageFont
from pprint import pprint

# import shlex
import sys
# from enum import Enum

font_size = 40
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

        (w, h) = d.textsize(text, font = font)

        self.size = (w, h)


    def get_top_left (self, coord):
        x, y = coord
        w, h = self.size
        return (x - 0.5 * w, y)


    def get_coord_below (self, coord):
        x, y = coord
        w, h = self.size
        return (x, y + h) # (x, y + 0.5 * h)


    def display (self):
        print("'" + self.text + "'" + " has size:")
        pprint(self.size)
 

  
    def draw (self, image, coord):
        top_left = self.get_top_left(coord)

        d = ImageDraw.Draw(image)

        d.text(top_left, self.text, font = font, fill = fill_color)


        return self.get_coord_below(coord)
        


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

    def TextDrawMultiline ():
        W, H = 2500, 1000
        i = Image.new("RGBA",(W,H),"white") # random
        lines = ["Yes", "Indeed", "This is a big long sentence which is very big and which is also very long"]
        
        s = '\n'.join(lines)
        coord = (W/2, 50)
        td = TextDraw(s)
        new_coord = td.draw(i, coord)
        i.show()
        pprint(new_coord)

    def TextDrawSeparateLines ():
        W, H = 2500, 1000
        i = Image.new("RGBA",(W,H),"white") # random
        lines = ["Yes", "Indeed", "This is a big long sentence which is very big and which is also very long"]
        
#        s = '\n'.join(lines)
        coord = (W/2, 50)

        for line in lines:
            td = TextDraw(line)
            coord = td.draw(i, coord)
            pprint(coord)

        i.show()






def main() -> int:
    Test.TextDrawMath()
    # Test.TextDrawMultiline()
    Test.TextDrawSeparateLines()


    return 0



if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
