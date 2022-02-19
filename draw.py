from PIL import Image, ImageDraw, ImageFont, ImageColor
from pprint import pprint

start_W, start_H = 3000, 2000

settings = {
    "font_style" : 'FreeMono.ttf',
    "font_size" : 80,
    "line_color" : '#000000',
    "thickness" : 4,

    "margin" : 50, # unused, todo
    "padding" : 20, # unused, todo
    "line_height" : int(start_H / 10),
    "default_width" : int(start_W * 0.2),     # width of top-level tree

    "size_test_W" : 10000,
    "size_test_H" : 10000,
    "W" : start_W, # whole image's width
    "H" : start_H, # whole image's height
    "coord" : (int(start_W / 2), 50) # starting coordinate (root node)
}



class TextDraw:
    def __init__ (self, text, cfg = settings):
        self.text = text
        self.cfg = cfg

        size_test_W = 10000
        size_test_H = 10000
        bg = "white"

        i = Image.new("RGBA",(size_test_W, size_test_H),"white") # random
        d = ImageDraw.Draw(i)

        self.font = ImageFont.truetype(self.cfg["font_style"], self.cfg["font_size"])
        (w, h) = d.textsize(text, font = self.font)

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

        print(self.cfg["line_color"])

        d.text(top_left,
               self.text,
               font = self.font,
               fill = ImageColor.getrgb(self.cfg["line_color"]))


        return self.get_coord_below(coord)
        





class LineDraw:
    def __init__ (self, top_point, delta_x, delta_y, cfg = settings):
        self.cfg = cfg

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


    def draw_line (self, image):
        d = ImageDraw.Draw(image)
        print(self.cfg["line_color"])

        d.line([self.top_point, self.bottom_point],
               fill = ImageColor.getrgb(self.cfg["line_color"]),
               width = self.cfg["thickness"])

        return self.bottom_point



    def draw_triangle (self, image):
        d = ImageDraw.Draw(image)
        fill_color = ImageColor.getrgb(self.cfg["line_color"])
        thickness = self.cfg["thickness"]

        d.line([self.top_point, self.bottom_point], fill_color, width = thickness)
        d.line([self.top_point, self.bottom_point_opposite], fill = fill_color, width = thickness)
        d.line([self.bottom_point, self.bottom_point_opposite], fill = fill_color, width = thickness)

        # return the *center* of the bottom line
        (top_x, top_y) = self.top_point
        return (top_x, top_y + self.delta_y)
