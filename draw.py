from PIL import Image, ImageDraw, ImageFont
from pprint import pprint




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
        





class LineDraw:
    def __init__ (self, top_point, delta_x, delta_y):
        self.top_point = top_point
        self.delta_x = delta_x
        self.delta_y = delta_y

        (top_x, top_y) = top_point

        self.bottom_point = (top_x + delta_x, top_y + delta_y) # right
        self.bottom_point_opposite = (top_x - delta_x, top_y + delta_y) # left

        

    def display (self):
        print("This line has top_point ")
        pprint(self.top_point)

        print("delta_x and delta_y are ")
        pprint((self.delta_x, self.delta_y))

        print("This line has bottom_point ")
        pprint(self.bottom_point)

        print("This line has bottom_point_opposite ")
        pprint(self.bottom_point_opposite)
