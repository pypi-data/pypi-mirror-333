# Generated from antlr4_grammar/hyconfiglanguage.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,8,53,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,4,1,
        4,1,4,1,4,1,4,1,4,1,4,1,5,1,5,5,5,38,8,5,10,5,12,5,41,9,5,1,6,4,
        6,44,8,6,11,6,12,6,45,1,7,1,7,4,7,50,8,7,11,7,12,7,51,0,0,8,1,1,
        3,2,5,3,7,4,9,5,11,6,13,7,15,8,1,0,2,3,0,65,90,95,95,97,122,4,0,
        48,57,65,90,95,95,97,122,55,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,
        0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,1,
        17,1,0,0,0,3,19,1,0,0,0,5,21,1,0,0,0,7,23,1,0,0,0,9,28,1,0,0,0,11,
        35,1,0,0,0,13,43,1,0,0,0,15,47,1,0,0,0,17,18,5,91,0,0,18,2,1,0,0,
        0,19,20,5,93,0,0,20,4,1,0,0,0,21,22,5,61,0,0,22,6,1,0,0,0,23,24,
        5,102,0,0,24,25,5,114,0,0,25,26,5,111,0,0,26,27,5,109,0,0,27,8,1,
        0,0,0,28,29,5,105,0,0,29,30,5,109,0,0,30,31,5,112,0,0,31,32,5,111,
        0,0,32,33,5,114,0,0,33,34,5,116,0,0,34,10,1,0,0,0,35,39,7,0,0,0,
        36,38,7,1,0,0,37,36,1,0,0,0,38,41,1,0,0,0,39,37,1,0,0,0,39,40,1,
        0,0,0,40,12,1,0,0,0,41,39,1,0,0,0,42,44,9,0,0,0,43,42,1,0,0,0,44,
        45,1,0,0,0,45,43,1,0,0,0,45,46,1,0,0,0,46,14,1,0,0,0,47,49,5,10,
        0,0,48,50,5,32,0,0,49,48,1,0,0,0,50,51,1,0,0,0,51,49,1,0,0,0,51,
        52,1,0,0,0,52,16,1,0,0,0,4,0,39,45,51,0
    ]

class hyconfiglanguageLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    NAME = 6
    VALUE = 7
    INDENT = 8

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'['", "']'", "'='", "'from'", "'import'" ]

    symbolicNames = [ "<INVALID>",
            "NAME", "VALUE", "INDENT" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "NAME", "VALUE", 
                  "INDENT" ]

    grammarFileName = "hyconfiglanguage.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


