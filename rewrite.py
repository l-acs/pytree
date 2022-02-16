from PIL import Image, ImageDraw, ImageFont
from enum import Enum

# two behaviors:
# for all leaves that are not triangles, either show a line between category and content or don't
# always show triangles


# for now, fix the padding and sizing for simplicity; refactor if lacking later
font_size = 32
font = ImageFont.truetype('FreeMono.ttf', font_size)
margin = 50

# likewise for thickness
thickness = 3

# how many pixels should vertically separate a node and its immediate children?
line_height = 30

# then just calculate and partition the horizontal space according to the number of children



class Write:
    def get_size_of (item):
        # figure out how big it would be to print this leaf with text aligned
        W = 10000
        H = 10000

        im = Image.new("RGBA",(W,H),"yellow") # random
        draw = ImageDraw.Draw(im)
        w, h = draw.textsize(item)

        # don't consider in intermediate lines for now (i.e. the line or triangle from category to content)

        return (w, h)


    def write_text (image, coordinate, text):
        # this is basically in the wrong class, but it will do for now

        # todo
        # steps:

        # 1) define cursor as coordinate_x and coordinate_y
        # 2) move cursor left by half width of text
        # 3) write text
        # 4) move cursor back to coordinate_x and (coordinate_y + text height)
        # 5) return cursor

        (cursor_x, cursor_y) = coordinate

        (size_w, size_h) = Write.get_size_of(text)

        # move cursor to where text should begin
        cursor_x -= (size_w / 2)


        d = ImageDraw.Draw(image)
        d.text((cursor_x, cursor_y), text, font=font, fill=(0, 0, 0))

        # move cursor back to center
        cursor_x += (size_w / 2)

        # move cursor down to below text
        cursor_y += size_h 

        # return the *cursor*!
        return (cursor_x, cursor_y)
        # N.B. this does not pad height, yet




class Shape(Enum):
    EMPTY = 0,
    LINE = 1,
    TRIANGLE = 3


class Line:
    def __init__ (self, shape):
        self.shape = shape


    def write_none (self, image, coordinate, delta_x = 0):
        return coordinate
        # only really here as a conceptual aid

    def write_line (self, image, coordinate, delta_x = 0):
        out_x, out_y = coordinate
        out_x += delta_x
        out_y += line_height

        # todo: actually draw
        # from coordinate to (out_x, out_y)

        # untested attempt at that:
        d = ImageDraw.Draw(image)
        d.line([coordinate, (out_x, out_y)], fill = None, width = thickness)



        return (out_x, out_y) # updated cursor



    def write_triangle (self, image, coordinate, delta_x = 0):
        (start_x, start_y) = coordinate


        
        left_x = start_x - delta_x
        right_x = start_x + delta_x
        y = start_y + line_height

        # todo: draw
        # from coordinate to (left_x, y)
        # from coordinate to (right_x, y)

        # untested attempt at that:
        d = ImageDraw.Draw(image)
        d.line([coordinate, (left_x, y)], fill = None, width = thickness)
        d.line([coordinate, (right_x, y)], fill = None, width = thickness)



        # triangles only apply to (effective) leaves, so cursor should not move left or right
        return (start_x, y) # updated cursor



    def draw (self, image, coordinate, delta_x = 0):
        # does this need to be something to the effect of
        # Shape.(self.shape)
        # ?

        if (self.shape.value == 3):
            return self.write_triangle(image, coordinate, delta_x)

        if (self.shape.value == 1):
            return self.write_line(image, coordinate, delta_x)

        if (self.shape.value == 0):
            return self.write_none(image, coordinate)



class Leaf:
    def __init__ (self, category, content, line = Line(Shape.EMPTY)):
        self.category = category
        self.content = content
        self.line = line


    def write (self, image, coordinate):
        cursor = Write.write_text(image, coordinate, self.category)

        cursor = self.line.draw(image, cursor, 0) # a leaf shouldn't represent a x-axis change

        cursor = Write.write_text(image, cursor, self.content)

        return cursor





class Tree:
    def __init__ (self, children):
        self.children = children



    # every child is either a leaf or a tree




def __main__ (__argv__):
    # lol I don't think this is right

    ex1 = Leaf("D", "John", Line(Shape.TRIANGLE)) # this doesn't raise an exception
    ex2 = Leaf("D", "John", Line(Shape.LINE)) # this does
    ex3 = Leaf("D", "John") # and so does this

    W, H = 1000, 1000
    image = Image.new("RGBA",(W,H),"white") # random


    ex3.write(image, (200, 200))

    image.show()



    return
