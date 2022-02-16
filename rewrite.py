from PIL import Image, ImageDraw, ImageFont
from enum import Enum

# two behaviors:
# for all leaves that are not triangles, either show a line between category and content or don't
# always show triangles


# for now, fix the padding and sizing for simplicity; refactor if lacking later
font_size = 32
font = ImageFont.truetype('FreeMono.ttf', font_size)
margin = 50

# how many pixels should vertically separate a node and its immediate children?
line_height = 30

# then just calculate and partition the horizontal space according to the number of children


class Shape(Enum):
    EMPTY = 0,
    LINE = 1,
    TRIANGLE = 3


class Line:
    def __init__ (self, shape):
        self.shape = shape


    def write_none (image, coordinate, delta_x = 0):
        return coordinate
        # only really here as a conceptual aid

    def write_line (image, coordinate, delta_x = 0):
        # todo: draw


        out_x, out_y = coordinate
        out_x += delta_x
        out_y += line_height

        return (out_x, out_y) # updated cursor



    def write_triangle (image, coordinate, delta_x = 0):
        # todo: draw



        out_x, out_y = coordinate

        # only applies to leaves, so cursor should not move left or right
        out_y += line_height
        return (out_x, out_y) # updated cursor



    def draw (image, coordinate, delta_x = 0):
        if (self.shape == 3):
            return write_triangle(image, coordinate, delta_x)

        if (self.shape == 1):
            return write_line(image, coordinate, delta_x)

        if (self.shape == 0):
            return write_none(image, coordinate)



class Leaf:
    def __init__ (self, category, content, line = 0)
        self.category = category
        self.content = content
        self.line = line


    def get_size_of (item):
        # figure out how big it would be to print this leaf with text aligned
        W = 10000
        H = 10000

        im = Image.new("RGBA",(W,H),"yellow") # random
        draw = ImageDraw.Draw(im)
        w, h = draw.textsize(item)

        # don't consider in intermediate lines for now (i.e. the line or triangle from category to content)

        return (w, h)

    def get_category_size ():
        return get_size_of(self.category)

    def get_content_size ():
        return get_size_of(self.content)


    def get_text_size (intermediate_line = False):
        (category_w, category_h) = self.get_category_size()
        (content_w, content_h) = self.get_content_size()

        # (text_w, text_y) = (category_w + content_w,
        #                     category_h + content_h)

        w = max(category_w, content_w)
        h = category_h + content_h

        if (line == 1 or line == 3)
            h += line_height

        return (w, h)






    def write_text (image, coordinate):
        # todo
        # steps:

        # 1) define cursor as coordinate_x and coordinate_y
        # 2) move cursor left by half width of category
        # 3) write category
        # 4) move cursor back to coordinate_x and (coordinate_y + line_height)
        # 5) move cursor left by half width of content
        # 6) write content


        image.text((cursor_x, cursor_y), this.category, font=font, fill =(255, 0, 0))

#        cursor_x = (width




        # return the *cursor*!
        return






    def write (image, coordinate):
        cursor = write_text(image, coordinate, self.category)

        cursor = line.draw(image, cursor, 0) # a leaf shouldn't represent a x-axis change

        cursor = write_text(image, cursor, self.content)

        return cursor





class Tree:
    def __init__ (self, children):
        self.children = children



    # every child is either a leaf or a tree
