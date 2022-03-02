from PIL import Image, ImageDraw, ImageFont, ImageColor
from pprint import pprint

font_dir = "fonts/"

settings = {
    "font_style" : 'Courier New',
    "font_size" : 22,

    "thickness" : 4,
    "fg_color" : '#000000',
    "bg_color" : '#ffffff',

    "margin" : 20,
    "top_padding" : 10, # between a parent node and its branch(es)
    "bottom_padding" : 20, # between a branch and the child

    "W" : 2500, # whole image's width
    "H" : 1700, # whole image's height
    "font_max_height_in_pixels" : None, # this is for internal use; it gets set in node.py
    "font_typical_word_width_in_pixels" : None # likewise
}



class TextDraw:
    def __init__ (self, text, cfg = settings):
        self.text = text
        self.cfg = cfg

        bg = "white"

        i = Image.new("RGBA",(cfg["W"], cfg["H"]),"white")
        d = ImageDraw.Draw(i)

        self.font = ImageFont.truetype(font_dir + self.cfg["font_style"] + '.ttf', self.cfg["font_size"] * 3)
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

        d.text(top_left,
               self.text,
               font = self.font,
               fill = ImageColor.getrgb(self.cfg["fg_color"]))


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

        d.line([self.top_point, self.bottom_point],
               fill = ImageColor.getrgb(self.cfg["fg_color"]),
               width = self.cfg["thickness"])

        return self.bottom_point



    def draw_triangle (self, image):
        d = ImageDraw.Draw(image)
        fill_color = ImageColor.getrgb(self.cfg["fg_color"])
        thickness = self.cfg["thickness"]

        d.line([self.top_point, self.bottom_point], fill_color, width = thickness)
        d.line([self.top_point, self.bottom_point_opposite], fill = fill_color, width = thickness)
        d.line([self.bottom_point, self.bottom_point_opposite], fill = fill_color, width = thickness)

        # return the *center* of the bottom line
        (top_x, top_y) = self.top_point
        return (top_x, top_y + self.delta_y)
