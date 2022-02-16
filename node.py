from PIL import Image, ImageDraw, ImageFont
# from pprint import pprint
from draw import TextDraw, LineDraw, line_height
from pprint import pprint

connect_categories_and_words = False
# sort of works when True, the line still cuts through them

connect_categories_and_words = True

# so the recursion works but it's not properly moving the cursor
class Node:
    def __init__ (self, text, children, is_triangle = False):
        self.text = text
        self.children = children # themselves just nodes!
        self.is_triangle = is_triangle
        self.child_count = len(children)
        self.horizontal_space = 200 * self.child_count # todo: possibly parameterize, or, better, calculate based on text sizes


    def display(self): # for testing, basically
        pprint(self.text)
        print("Triangle? " + str(self.is_triangle))
        print("I have " + str(self.child_count) + " immediate child(ren): ")
        for child in self.children:
            child.display()
        print('---' * 20)


    def draw_node (self, image, coord):
        # todo: figure out where/how d_x comes into play

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

            # first, draw the text

            # now, connect if applicable
            if (self.is_triangle): # draw a triangle
              d_x = 50 # super arbitrary, todo: fix

              d_y = line_height

              line = LineDraw(acc_coord, d_x, d_y)
              acc_coord = line.draw_triangle(image)



            elif (connect_categories_and_words): # draw a line
              d_x = 0 # straight line down, so no change in x
              d_y = line_height

              line = LineDraw(coord, d_x, d_y)
              acc_coord = line.draw_line(image)

            # now draw the subsequent text
            text = ' '.join([child.text for child in self.children])
            td = TextDraw(text) # does this need to be a new one?
            acc_coord = td.draw(image, acc_coord)

        elif (self.child_count == 1): # one child with its own children
            # draw left
            d_x = 0 # straight line down, so no change in x
            d_y = line_height
            
            line = LineDraw(acc_coord, d_x, d_y)
            acc_coord = line.draw_line(image)

            # recurse
            self.children[0].draw_node(image, acc_coord)
                        

        else: # this means there's complex children
            # for child in self.children:

            # todo: draw line! this doesn't draw lines on its own


            # draw left
            d_x = 50
            d_y = line_height
            
            # left:
            line = LineDraw(acc_coord, -1 * d_x, d_y)
            acc_coord_left = line.draw_line(image)

            
            # now draw the subsequent text
            td = TextDraw(self.text) # does this need to be a new one?
            acc_coord_left = td.draw(image, acc_coord_left)



            # right:
            line = LineDraw(acc_coord, d_x, d_y)
            acc_coord_right = line.draw_line(image)


            # recurse
            self.children[0].draw_node(image, acc_coord_left) # todo: figure out x-axis movement
            self.children[1].draw_node(image, acc_coord_right) # todo: figure out x-axis movement




        return acc_coord

