# https://github.com/pyparsing/pyparsing/blob/master/examples/jsonParser.py

import pyparsing as pp
from pyparsing import pyparsing_common as ppc

# set to False to return ParseResults
RETURN_PYTHON_COLLECTIONS = True

delims =  "<>[]"
LANGLE, RANGLE, LBRACK, RBRACK = map(pp.Suppress, delims)

label = pp.Word(pp.printables, exclude_chars=delims) #dblQuotedString().setParseAction(pp.removeQuotes)
# formerly jsonString

tree = pp.Forward().setName("tree") # formerly jsonObject
node = pp.Forward().setName("node") # formerly jsonValue

# jsonElements = pp.delimitedList(node).setName(None)

# triangle = pp.Group( # not working right
#     LANGLE + pp.Optional(jsonElements) + RANGLE, aslist=RETURN_PYTHON_COLLECTIONS
# ).setName("triangle")
# # formerly "jsonArray"
triangle = pp.Forward().setName("triangle")




node << (label | tree | triangle)


treeMemberDef = pp.Group(
    label + pp.ZeroOrMore(node), aslist=RETURN_PYTHON_COLLECTIONS
).setName("treeMember")

treeMembers = pp.delimitedList(treeMemberDef).setName(None)

triangleMemberDef = pp.Group(
    # todo: add some kind of boolean flag
    label + pp.ZeroOrMore(node), aslist=RETURN_PYTHON_COLLECTIONS
).setName("triangleMember")

triangleMembers = pp.delimitedList(treeMemberDef).setName(None)


tree << pp.Dict(
    LBRACK + pp.Optional(treeMembers) + RBRACK, asdict=RETURN_PYTHON_COLLECTIONS
)

triangle << pp.Combine(
    LANGLE + pp.Optional(treeMembers) + RANGLE, adjacent=False
).setParseAction(pp.removeQuotes)
                 #with_attribute(is_triangle=True))
# triangle << pp.Group(
#     LANGLE + pp.Optional(treeMembers) + RANGLE
# ).setParseAction(pp.with_attribute(is_triangle = True))



# idea: if it's a list, not a dict, then we know it's a triangle
# that's intuitive, right?

# formerly "jsonArray"


# it works! but it doesn't distinguish between them... hmm


def parse (s):
    return tree.parseString(s)


if __name__ == "__main__":
    testdata = """
    [Here is]
    """

    results = tree.parseString(testdata)

    
    sample = "[NP [D the] [N' <AdjP very big> [N dog]]]" # fails
    # but without the angle brackets it succeeds

    parse("[NP [DP [D the] [D 30]] [N' [AdjP very big] [N dogs]]]")
    parse("[]")

    results.pprint()
    if RETURN_PYTHON_COLLECTIONS:
        from pprint import pprint

        pprint(results)
    else:
        results.pprint()
    print()

