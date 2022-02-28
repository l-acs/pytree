from PIL import Image, ImageDraw
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

        # how many layers deep do I go?
        self.number_of_generations_below = 1 \
            if self.child_count == 0 \
               else 1 + max([immediate_child.number_of_generations_below for immediate_child in self.children])


    def display(self, indent = ''): # for testing, basically
        print(indent + self.text + " has " + str(self.child_count) + " immediate child(ren)." + "Triangle?" + str(self.is_triangle))
        for child in self.children:
            child.display(indent + ' ' * 4)
        print('---' * 20)


    def calculate_initial_node_x (self, cfg = settings):
        # this means it's the first call!
        if self.child_count == 1: # since it has exactly one child, we have to check and recurse on it
            left = self.children[0]
            return left.calculate_initial_node_x(cfg)

        # otherwise...
        if self.child_count == 0: # edge case: this (sub)tree doesn't branch at all; we're just midway
            return cfg["W"] / 2

        else:
            left_count = self.children[0].all_terminal_children_count
            ratio = left_count / (self.all_terminal_children_count - left_count) # left vs non-left

            drawable_x = cfg["drawable_width"] / 2
            # print(f"The ratio is {ratio} and the margin is {cfg['margin']}; x is {drawable_x}")
            drawable_x *= ratio
            drawable_x += cfg["margin"] + (cfg["font_typical_word_width_in_pixels"] / 2)
            # print("so our coordinate will be " + str(drawable_x))
            return drawable_x


    def determine_line_height (self, cfg = settings):
        # set the branch height
        full_image_height_sans_margin = cfg["H"] - (2 * cfg["margin"])
        # print(cfg["font_max_height_in_pixels"])
        text_height = cfg["font_max_height_in_pixels"]  + cfg["top_padding"] + cfg["bottom_padding"]

        return (full_image_height_sans_margin / self.number_of_generations_below) - text_height


    def initialize_root (self, cfg = settings):
        # when we call draw_node on a root, we have to preprocess the tree in a sense

        (cfg["font_typical_word_width_in_pixels"],
         cfg["font_max_height_in_pixels"]) = TextDraw("LARGE TEXT", cfg).size

        cfg["line_height"] = self.determine_line_height(cfg)
        cfg["drawable_width"] = cfg["W"] - 2 * (cfg["margin"] + cfg["font_typical_word_width_in_pixels"]) # what width we can actually draw *nodes* on

        return


    def draw_node (self, image, cfg = settings, coord = None, width = None):
        # determine width of branches
        if width == None: # this is the tree root, so let's initialize some things
            self.initialize_root(cfg)

            # try: take advantage of that sum thing
            # width is the x-axis movement left or right of the first node at which our tree branches
            full_image_width_sans_margin = cfg["drawable_width"]
            # print(f"The width the tree can fill is {full_image_width_sans_margin}")
            width = full_image_width_sans_margin / 4

            # for a rainy day, consider this:
            # this is so close to being exactly what we want
            # the problem is that it doesn't prevent text collsion between two nodes being too close together
            # maybe we need to somehow set a *minimum* width



        if coord == None: # first call, so we have to determine where the root should go
            coord = (self.calculate_initial_node_x(cfg), cfg["margin"])

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
              d_y = cfg["line_height"] - cfg["top_padding"]

              line = LineDraw(coord, d_x, d_y, cfg)
              acc_coord = line.draw_line(image)
              # todo: add back the padding here (?))

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
