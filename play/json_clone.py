# https://github.com/pyparsing/pyparsing/blob/master/examples/jsonParser.py

import pyparsing as pp
from pyparsing import pyparsing_common as ppc


def make_keyword(kwd_str, kwd_value):
    return pp.Keyword(kwd_str).setParseAction(pp.replaceWith(kwd_value))


# set to False to return ParseResults
RETURN_PYTHON_COLLECTIONS = True

TRUE = make_keyword("true", True)
FALSE = make_keyword("false", False)
NULL = make_keyword("null", None)

delims =  "<>[]"
LANGLE, RANGLE, LBRACK, RBRACK = map(pp.Suppress, delims)

nodeLabel = pp.Word(pp.printables, exclude_chars=delims) #dblQuotedString().setParseAction(pp.removeQuotes)
jsonNumber = ppc.number().setName("jsonNumber")

jsonObject = pp.Forward().setName("jsonObject")
jsonValue = pp.Forward().setName("jsonValue")

jsonElements = pp.delimitedList(jsonValue).setName(None)

jsonArray = pp.Group(
    LANGLE + pp.Optional(jsonElements) + RANGLE, aslist=RETURN_PYTHON_COLLECTIONS
).setName("jsonArray")

jsonValue << (nodeLabel | jsonNumber | jsonObject | jsonArray | TRUE | FALSE | NULL)

memberDef = pp.Group(
    nodeLabel + pp.ZeroOrMore(jsonValue), aslist=RETURN_PYTHON_COLLECTIONS
).setName("jsonMember")

jsonMembers = pp.delimitedList(memberDef).setName(None)
# jsonObject << pp.Dict(LBRACK + pp.Optional(jsonMembers) + RBRACK)
jsonObject << pp.Dict(
    LBRACK + pp.Optional(jsonMembers) + RBRACK, asdict=RETURN_PYTHON_COLLECTIONS
)


if __name__ == "__main__":
    testdata = """
    [Here is]
    """

    results = jsonObject.parseString(testdata)

    
    sample = "[NP [D the] [N' <AdjP very big> [N dog]]]" # fails
    # but without the angle brackets it succeeds



    results.pprint()
    if RETURN_PYTHON_COLLECTIONS:
        from pprint import pprint

        pprint(results)
    else:
        results.pprint()
    print()

    def testPrint(x):
        print(type(x), repr(x))

    if RETURN_PYTHON_COLLECTIONS:
        results = results[0]
        print(list(results["glossary"]["GlossDiv"]["GlossList"][0].keys()))
        testPrint(results["glossary"]["title"])
        testPrint(results["glossary"]["GlossDiv"]["GlossList"][0]["ID"])
        testPrint(results["glossary"]["GlossDiv"]["GlossList"][0]["FalseValue"])
        testPrint(results["glossary"]["GlossDiv"]["GlossList"][0]["Acronym"])
        testPrint(
            results["glossary"]["GlossDiv"]["GlossList"][0]["EvenPrimesGreaterThan2"]
        )
        testPrint(results["glossary"]["GlossDiv"]["GlossList"][0]["PrimesLessThan10"])
    else:
        print(list(results.glossary.GlossDiv.GlossList.keys()))
        testPrint(results.glossary.title)
        testPrint(results.glossary.GlossDiv.GlossList.ID)
        testPrint(results.glossary.GlossDiv.GlossList.FalseValue)
        testPrint(results.glossary.GlossDiv.GlossList.Acronym)
        testPrint(results.glossary.GlossDiv.GlossList.EvenPrimesGreaterThan2)
        testPrint(results.glossary.GlossDiv.GlossList.PrimesLessThan10)
