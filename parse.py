import pyparsing as pp
# many thanks to this example:
# https://github.com/pyparsing/pyparsing/blob/master/examples/jsonParser.py

# docs here
# https://pyparsing-docs.readthedocs.io/en/latest/HowToUsePyparsing.html#usage-notes
class Parse:
    RETURN_PYTHON_COLLECTIONS = True # set to False to return ParseResults instead

    delims =  "<>[]"
    LANGLE, RANGLE, LBRACK, RBRACK = map(pp.Suppress, delims)


    label = pp.Word(pp.printables, exclude_chars=delims) # formerly jsonString

    tree = pp.Forward().setName("tree") # formerly jsonObject
    node = pp.Forward().setName("node") # formerly jsonValue
    triangle = pp.Forward().setName("triangle") # formerly "jsonArray"


    node << (label | tree | triangle)


    memberDef = pp.Group(
        label + pp.ZeroOrMore(node), aslist=RETURN_PYTHON_COLLECTIONS
    ).setName("treeMember")

    treeMembers = pp.delimitedList(memberDef).setName(None)

    tree << pp.Dict(
        LBRACK + pp.Optional(treeMembers) + RBRACK, asdict=RETURN_PYTHON_COLLECTIONS
    )
    
    triangle << pp.Combine(
        LANGLE + pp.original_text_for(pp.Optional(treeMembers)) + RANGLE, adjacent=False
        # N.B.: anything below a triangle is treated literally, even if it would otherwise form valid tree or triangle data
    )

    def parse (s):
        return (Parse.tree).parseString(s)


# once we actually turn this into nodes, we can just set the
# is_triangle flag to be True dynamically

# if we're trying to create nodes and find a string in place of a dict,
# instead of making a node based on just that,
# - split that along the first space into `category` (left) and `rest` (right)
# - make a triangle node s.t.
#   - its text = `category` and
#   - its only child is a (childless) node with the text `rest`



if __name__ == "__main__":
# def __main__ ():
    testdata = """
    [Here is]
    """

    results = tree.parseString(testdata)

    
    sample = "[NP [D the] [N' <AdjP very big> [N dog]]]"

    print(
        parse("[NP [DP [D the] [D 30]] [N' [AdjP very big] [N dogs]]]"))

    print(
        parse("[NP [DP [D the] [D 30]] [N' [AdjP <AdvP very very very> [A big]] [N dogs]]]"))

    print(
        parse("[]"))


    print(
        parse("[IP [NP [DP [D the] [D 30]] [N' [AdjP very big] [N dogs]]] [I' [I will] [VP [V be] [P here]]]]")
    )
