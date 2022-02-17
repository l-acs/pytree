# https://github.com/pyparsing/pyparsing/blob/master/examples/jsonParser.py

import pyparsing as pp
from pyparsing import pyparsing_common as ppc

# set to False to return ParseResults
RETURN_PYTHON_COLLECTIONS = True

delims =  "<>[]"
LANGLE, RANGLE, LBRACK, RBRACK = map(pp.Suppress, delims)

label = pp.Word(pp.printables, exclude_chars=delims) #dblQuotedString().setParseAction(pp.removeQuotes)
# formerly jsonString

tree = pp.Forward().setName("tree")
node = pp.Forward().setName("node")

jsonElements = pp.delimitedList(node).setName(None)

triangle = pp.Group( # not working right
    LANGLE + pp.Optional(jsonElements) + RANGLE, aslist=RETURN_PYTHON_COLLECTIONS
).setName("triangle")
# formerly "jsonArray"

node << (label | tree | triangle)
# formerly jsonValue


memberDef = pp.Group(
    label + pp.ZeroOrMore(node), aslist=RETURN_PYTHON_COLLECTIONS
).setName("jsonMember")

jsonMembers = pp.delimitedList(memberDef).setName(None)

tree << pp.Dict(
    LBRACK + pp.Optional(jsonMembers) + RBRACK, asdict=RETURN_PYTHON_COLLECTIONS
)


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

