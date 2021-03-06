import pygments
from pygments.lexers import Python3Lexer

from constants import SyntaxColors, Colors
import Util.editorUtil as editorUtil

# testing
from Util.cursesUtil import kill


def setColors(editorObj, colorMap):
    """
    Sets the colors of the editorObj for every line
    in editorObj.lineLinkedList.

    Assumes every file is a python file, need to use
    different lexers later (possibly check with something
    else then pass it in as an argument).

    colorMap is a dictionary which maps the kind of syntax
    to a certain color.

    Use this with editorscr only!

    Notice that this won't work perfectly; there will be times that
    the syntax highlighting won't be perfect. This is a decided tradeoff;
    the popular text editors don't seem to have a solution.
    """
    pylex = Python3Lexer(stripnl = False, stripall=False)
    # lets build the string to parse

    syntax = ''
    walk = editorObj.lineLinkedList.start
    y = 0
    increaseY = False
    while walk is not None:
        if walk == editorObj.currentLine:
            increaseY = True
        syntax += walk.value
        if increaseY:
            y += editorUtil.lineHeight(editorObj.editorscr, walk)
        if y > editorObj.editorscr.getmaxyx()[0]:
            break
        walk = walk.nextNode

    walk = editorObj.lineLinkedList.start
    i = 0 # index of where i am walking through the string

    #kill(editorObj)
    #for token in pylex.get_tokens(syntax):
    #    print(token,end='\r\n')
    #assert(False)

    for token in pylex.get_tokens(syntax):

        if token[1] == '\n':
            walk = walk.nextNode
            #i = -1
            i = 0
            if walk is None:
                break
            continue

        tokenType = colorMap['TEXT'] # assume everything is text and find contradiction

        if pygments.token.Comment.Single is token[0]:
            tokenType = colorMap['COMMENT']

        if pygments.token.Keyword.Namespace is token[0]:
            tokenType = colorMap['NAMESPACE']

        if pygments.token.Keyword is token[0]:
            tokenType = colorMap['KEYWORD']

        if pygments.token.Name.Builtin is token[0]:
            tokenType = colorMap['BUILTIN']

        if pygments.token.Name.Function is token[0]:
            tokenType = colorMap['FUNCTION']

        if pygments.token.Literal.Number.Integer is token[0] or pygments.token.Literal.Number.Float is token[0]:
            tokenType = colorMap['LITERAL']

        if pygments.token.Operator is token[0]:
            tokenType = colorMap['OPERATOR']

        if (pygments.token.Literal.String.Single is token[0] or
                    pygments.token.Literal.String.Double is token[0]):
            tokenType = colorMap['STRING_LITERAL']

        if pygments.token.Literal.String.Doc is token[0]:
                tokenType = colorMap['STRING_LITERAL']

        if token[0] is pygments.token.Literal.String.Doc:
            for tok in token[1].split('\n'):
                for c in tok:
                    try:
                        walk.colors[i] = tokenType
                    except:
                        a = 1 # do nothing
                    i += 1
                i = 0
                walk = walk.nextNode

            # if we were at the end break
            if walk is None:
                break

            # set everything back to the way it was before
            walk = walk.lastNode
            i = -1
            continue

        for c in token[1]:
            try:
                walk.colors[i] = tokenType
                i += 1
            except:
                a = 1 # do nothing
