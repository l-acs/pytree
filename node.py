from PIL import Image, ImageDraw
# from pprint import pprint
from draw import TextDraw, LineDraw, settings
from pprint import pprint

connect_categories_and_words = False

# connect_categories_and_words = True
# when True, the line cuts through the category
# (it goes directly from its branch down through the middle of the category and up until the terminal text )

def pad_coord (coord, pad_x = 0, pad_y = 0):
    x, y = coord
    return (x + pad_x, y + pad_y)



class Node:
    def __init__ (self, text, children = [], is_triangle = False):
        self.text = text
        self.children = children # themselves just nodes!
        self.is_triangle = is_triangle
        self.child_count = len(children)

        self.all_terminal_children_count = 1 \
            if self.child_count == 0 \
               else sum([immediate_child.all_terminal_children_count for immediate_child in self.children])

    def display(self, indent = ''): # for testing, basically
        print(indent + self.text + " has " + str(self.child_count) + " immediate child(ren)." + "Triangle?" + str(self.is_triangle))
        for child in self.children:
            child.display(indent + ' ' * 4)
        print('---' * 20)


    def draw_node (self, image, cfg = settings, coord = None, width = None):

        if width == None:
            width = cfg["default_width"]

        if coord == None:
            coord = cfg["coord"] # this means it's the first call!

        else: # it's not the first call, and we should pad it (because i.e. there's a line before it)
            coord = pad_coord(coord, pad_y = cfg["bottom_padding"])

        td = TextDraw(self.text, cfg)


        # just start by drawing the text
        acc_coord = td.draw(image, coord)

        # now pad before the lines (after the text we just wrote)
        # i.e. add padding between parent node's text and its branches
        acc_coord = pad_coord(acc_coord, pad_y = cfg["top_padding"])
        
        
        if (self.child_count == 0): # it's terminal
            return acc_coord # done

        elif ((self.child_count == 1 and self.children[0].child_count == 0) or self.is_triangle):
            # there's this node and one more, and the next node is terminal
            # this means that this node is a category and the other node is text
            # _or_, it means that there's multiple children and it's a triangle


            # now, connect if applicable
            if (self.is_triangle): # draw a triangle
              d_x = width

              d_y = cfg["line_height"]

              line = LineDraw(acc_coord, d_x, d_y, cfg)
              acc_coord = line.draw_triangle(image)


            elif (connect_categories_and_words): # draw a line
              d_x = 0 # straight line down, so no change in x
              d_y = cfg["line_height"]

              line = LineDraw(coord, d_x, d_y, cfg)
              acc_coord = line.draw_line(image)

            # now draw the subsequent text
            text = ' '.join([child.text for child in self.children])
            td = TextDraw(text, cfg) # does this need to be a new one?

            # now draw the text, padded
            acc_coord = td.draw(image, pad_coord(acc_coord, pad_y = cfg["bottom_padding"]))
            # bottom because we just drew a line

            # it only gets reassigned for the sake of the return value

        elif (self.child_count == 1): # one child with its own children
            # draw left
            d_x = 0 # straight line down, so no change in x
            d_y = cfg["line_height"]
            
            line = LineDraw(acc_coord, d_x, d_y, cfg)
            acc_coord = line.draw_line(image)

            # recurse
            self.children[0].draw_node(image, cfg, acc_coord, width)
                        

        else: # this means there's complex children

            # ideally, this should somehow be `for child in self.children`
            # binary only for now

            # draw left
            d_x = width
            d_y = cfg["line_height"]
            
            # left:
            line_left = LineDraw(acc_coord, -1 * d_x, d_y, cfg)
            acc_coord_left = line_left.draw_line(image)

            # right:
            line_right = LineDraw(acc_coord, d_x, d_y, cfg)
            acc_coord_right = line_right.draw_line(image)
            
            left = self.children[0]
            right = self.children[1]
            
            # recurse
            left.draw_node(image, cfg, acc_coord_left,
                           width * (left.all_terminal_children_count) / self.all_terminal_children_count)

            right.draw_node(image, cfg, acc_coord_right,
                           width * (right.all_terminal_children_count) / self.all_terminal_children_count)


        return acc_coord # not sure this matters
