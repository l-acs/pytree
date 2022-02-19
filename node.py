from PIL import Image, ImageDraw
# from pprint import pprint
from draw import TextDraw, LineDraw, settings
from pprint import pprint

connect_categories_and_words = False

# connect_categories_and_words = True
# when True, the line cuts through the category
# (it goes directly from its branch down through the middle of the category and up until the terminal text )

class Node:
    def __init__ (self, text, children = [], is_triangle = False):
        self.text = text
        self.children = children # themselves just nodes!
        self.is_triangle = is_triangle
        self.child_count = len(children)

        self.all_terminal_children_count = 1 \
            if self.child_count == 0 \
               else sum([immediate_child.all_terminal_children_count for immediate_child in self.children])

    def display(self): # for testing, basically
        pprint(self.text)
        print("Triangle? " + str(self.is_triangle))
        print("I have " + str(self.child_count) + " immediate child(ren): ")
        for child in self.children:
            child.display()
        print('---' * 20)


    def draw_node (self, image, cfg = settings, coord = None, width = None):

        if width == None:
            width = cfg["default_width"]

        if coord == None:
            coord = cfg["coord"]

        td = TextDraw(self.text)
        acc_coord = td.draw(image, coord) # just start by drawing the text
        
        
        if (self.child_count == 0):
            return acc_coord # done

            # td.draw(image, coord)
        # elif
        elif ((self.child_count == 1 and self.children[0].child_count == 0) or self.is_triangle):
            # there's this node and one more, and the next node is terminal
            # this means that this node is a category and the other node is text
            # _or_, it means that there's multiple children and it's a triangle


            # now, connect if applicable
            if (self.is_triangle): # draw a triangle
              d_x = width

              d_y = cfg["line_height"]

              line = LineDraw(acc_coord, d_x, d_y)
              acc_coord = line.draw_triangle(image)



            elif (connect_categories_and_words): # draw a line
              d_x = 0 # straight line down, so no change in x
              d_y = cfg["line_height"]

              line = LineDraw(coord, d_x, d_y)
              acc_coord = line.draw_line(image)

            # now draw the subsequent text
            text = ' '.join([child.text for child in self.children])
            td = TextDraw(text) # does this need to be a new one?
            acc_coord = td.draw(image, acc_coord)

        elif (self.child_count == 1): # one child with its own children
            # draw left
            d_x = 0 # straight line down, so no change in x
            d_y = cfg["line_height"]
            
            line = LineDraw(acc_coord, d_x, d_y)
            acc_coord = line.draw_line(image)

            # recurse
            self.children[0].draw_node(image, cfg, acc_coord, width) # width / 2)
            # see what happens if we don't reduce width of non-branching children
                        

        else: # this means there's complex children

            # ideally, this should somehow be `for child in self.children`
            # binary only for now

            # draw left
            d_x = width
            d_y = cfg["line_height"]
            
            # left:
            line_left = LineDraw(acc_coord, -1 * d_x, d_y)
            acc_coord_left = line_left.draw_line(image)

            # right:
            line_right = LineDraw(acc_coord, d_x, d_y)
            acc_coord_right = line_right.draw_line(image)
            
            left = self.children[0]
            right = self.children[1]
            
            # recurse
            left.draw_node(image, cfg, acc_coord_left,
                           width * (left.all_terminal_children_count) / self.all_terminal_children_count)

            right.draw_node(image, cfg, acc_coord_right,
                           width * (right.all_terminal_children_count) / self.all_terminal_children_count)


        return acc_coord
