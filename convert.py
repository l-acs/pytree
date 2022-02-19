# goal: go from
# [XP [X' [YP [Y' [Y your] [ZP [Z' [Z word]]]]]]]
# to a tree. Etc.

import sys
from parse import Parse as p
from node import Node, settings


# # okay, now link up node and ParseResults
# cases to handle
def leaf (text): # takes no children
    return Node(text)


def triangle (text):
    # assumes there's at least at least one space in text passed
    pieces = text.split(' ')
    category = pieces[0]
    children_text = pieces[1:]

    # text_as_leaf_nodes = [leaf(word) for word in children_text]
    # return Node(category, text_as_leaf_nodes, is_triangle=True)
    text_as_leaf_node = Node(children_text, [], True)
    # text_as_leaf_node = leaf(children_text)
    return Node(category, [text_as_leaf_node], True)


def is_triangle (text):
    text_pieces = text.split(' ')
    return len(text_pieces) > 1


def handle (label, item):
    # there is always a LHS and a RHS of a map entry
    # the LHS is always text
    # the RHS is either text, a list, or a one-entry dictionary

    t = type(item)
    handlers = {
        str : handle_text,
        dict : handle_dict,
        list : handle_list
    }

    return handlers[t](label, item)

def handle_text(label, text):
    # handle a leaf and its label, whether that leaf is a triangle or not

    if is_triangle(text):
        #        inner = triangle(text) # node
        #        return Node(label, [inner], True)
        return triangle(text)

    else:
        inner = leaf(text)
        return Node(label, [inner])


def handle_dict (label, d):
    # i.e. one child
    k, v = d.popitem()

    inner_node = handle(k, v)
    return Node(label, [inner_node])


def handle_list (label, l):
    # the only 'edge' case here is where regular brackets are used like triangles,
    # in which case we'd get a list of strings, not tuples
    # thus we can't just do:
    # sub_nodes = [handle(tup[0], tup[1]) for tup in l]

    sub_nodes = []

    for item in l:
        if (type(item) == str):
            node = leaf(item)
        else:
            k, v = item.popitem()
            node = handle(k, v)

        sub_nodes.append(node)
        

    return Node(label, sub_nodes)



class Convert:    
    def __init__ (self, string = None, parse_results = None):
        if (string != None):
            parse_results = p.parse(string)

        self.pr = parse_results
        self.root = self.to_root()

    def to_root (self):
        if (len(self.pr) != 1):
            return None # we require *exactly one* top-level tree
    
        return self.pr[0]
    
    
    def to_tree (self):
        cat, rest = self.root.popitem()
        return handle(cat, rest)
    
    
    # one issue exists: some triangles are not being recognized as triangles
    # more specifically, if a would-be triangle has a sister, it isn't recognized as being a triangle

def __nota_bene__():
    from pprint import pprint

    def bar():
        print('- ' * 20 + '-')

    print("N.B. the difference between a non-triangle and a triangle, when taking multiple arguments:")
    pprint(Convert("[DP [D' my dear old friend]]").root)
    # >>> {'DP': {"D'": ['my', 'dear', 'old', 'friend']}}

    pprint(Convert("[DP <D' my dear old friend>]").root)
    # >>> {'DP': "D' my dear old friend"}

    bar()
    print("and when taking a single argument:")
    pprint(Convert("[DP [D' John]]").root)
    # >>>> {'DP': {"D'": 'John'}}

    pprint(Convert("[DP <D' John>]").root)
    # >>> {'DP': "D' John"}

    bar()
    print("Therefore, a dictionary whose value is a multi-word string is guaranteed to be a triangle,")
    print("and a dictionary whose value is a list of strings is guaranteed to represent a node with a")
    print("single category and two or more leaf children.")
    print("(The latter has no meaning to my knowledge but is possible.)")



if __name__ == "__main__":
    W, H = 2500, 1000
    coord = (W/2, 50)

    from PIL import Image
    image = Image.new("RGBA",(W,H),"white") # random

    s = "[IP [NP [DP [D the] [D 30]] [N' [AdjP very big] [N dogs]]] [I' [I will    ] [VP [V be] [P here]]]]"
    pr = p.parse(s)

    tree = Convert(parse_results = pr).to_tree()

    tree.draw_node(image, coord)
    image.show()

    __nota_bene__()
