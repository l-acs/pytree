from pprint import pprint
# import shlex
import sys

from PIL import Image, ImageDraw, ImageFont
from draw import TextDraw, LineDraw
from node import Node, connect_categories_and_words



class Test:
    def __init__(self):
        None


    def TextDrawMath ():
        h = "Hello"
        td = TextDraw(h)
        td.display()
        print(20 * '---')

        lines = ["Yes", "Indeed", "This is a big long sentence which is very big and which is also very long"]

        coord = (100, 50)


        W, H = 1000, 1000
        i = Image.new("RGBA",(W,H),"white") # random



        for line in lines:
            td = TextDraw(line)
            td.display()
            print('Coord:')
            print(coord)
            print('Top left:')
            print(td.get_top_left(coord))
            print('Below:')
            print(td.get_coord_below(coord))

            print('After drawing:')
            pprint(td.draw(i, coord))
            print(20 * '---')
            

        TextDraw('\n'.join(lines))

    def TextDrawMultiline (image, coord):
        lines = ["Yes", "Indeed", "This is a big long sentence which is very big and which is also very long"]
        
        s = '\n'.join(lines)

        td = TextDraw(s)
        new_coord = td.draw(image, coord)
        pprint(new_coord)
        return new_coord

    def TextDrawSeparateLines (image, coord):
        lines = ["Yes", "Indeed", "This is a big long sentence which is very big and which is also very long"]
        
        # s = '\n'.join(lines)

        for line in lines:
            td = TextDraw(line)
            coord = td.draw(image, coord)
            pprint(coord)

        return coord


    def LineDrawMath ():
        print("hey")
        coord = (100, 50)


        W, H = 1000, 1000
        i = Image.new("RGBA",(W,H),"white") # random

        delta_x, delta_y = (50, 100)


        line = LineDraw(coord, delta_x, delta_y)

        line.display()


    def DrawLine (image, coord, d_x, d_y):
        line = LineDraw(coord, d_x, d_y)
        return line.draw_line(image)


    def DrawTriangle (image, coord, d_x, d_y):
        line = LineDraw(coord, d_x, d_y)
        return line.draw_triangle(image)


    def BuildNodes ():
        # not a nested structure, properly
        # it's just a dict
        sen = 'Jamie was wondering about the dog'.split(' ')

        nodes = {}

        node_names = ['a', 'b', 'c', 'd', 'e', 'f']

        prev = None
        sen_backwards = list(reversed(sen))
        print(sen)
        print(sen_backwards)
        for index, name in enumerate(node_names):

            if prev:
                nodes[name] = Node(sen_backwards[index], [prev])

            else:
                nodes[name] = Node(sen_backwards[index], [])

            prev = nodes[name]
            print("prev is type " + str(type(prev)))

        print(type(nodes['a']))
        return nodes
   
    def DrawNodeBaseZero (image, coord):
        # tree is a Node of nodes
        # base case: node with no children
        # nodes = BuildNodes()
        

        nodes = Test.BuildNodes()


        node = nodes['a']
        result = node.draw_node(image, coord)
        return result


    def DrawNodeBaseOne (image, coord):
        # tree is a Node of nodes
        # base case: node with one simple child
        nodes = Test.BuildNodes()


        node = nodes['b']
        result = node.draw_node(image, coord)
        return result




    def DrawNodeBaseTriangleZero (image, tree, coord):
        # tree is a Node of nodes
        # base case: triangle node with zero children
        result = coord

        return result

    def DrawNodeBaseTriangleOne (image, tree, coord):
        # tree is a Node of nodes
        # base case: triangle node with one child
        result = coord

        return result
        
    def DrawNodeBaseTriangleMany (image, tree, coord):
        # tree is a Node of nodes
        # base case: triangle node with many children
        result = coord

        return result
        

    def DrawNodeComplex (image, tree, coord):
        # tree is a Node of nodes
        # tree consists of complex children
        result = coord

        return result




def main() -> int:
    W, H = 2500, 1000
    i = Image.new("RGBA",(W,H),"white") # random

    Test.LineDrawMath()

    coord = (W/2, 50)
    # Test.DrawLine(i, coord, 300, 100)

    # out = Test.DrawLine(i, coord, 50, 200)
    # out = Test.DrawTriangle(i, out, 300, 100)
    # out = Test.TextDrawSeparateLines(i, out)
    # i.show()

    

    # pprint(nodes)
    #     # print(n)
    #     # print(n.text)
    #     # print(type(n))
    #     # # n.display()
#    nodes = Test.BuildNodes()
    # nodes = Test.nodes


    # for key in nodes:
    #     print(key)
    #     nodes[key].display()

    # Test.DrawNodeBaseZero(i, coord)
    Test.DrawNodeBaseOne(i, coord)


    i.show()

    return 0



if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
