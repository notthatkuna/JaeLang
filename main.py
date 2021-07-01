from ply import lex, yacc
import random

tokens = (
    'NUMBER',
    'ADD',
    'SUBTRACT',
    'MULTIPLY',
    'DIVIDE',
    'NAME',
    'GREET',
    'EQUALS',
    'STACKASCII',
    'LPAREN',
    'RPAREN',
    'EXPO'
)

t_ADD = r"\+"
t_SUBTRACT = r"\-"
t_MULTIPLY = r"\*"
t_DIVIDE = r"\/"
t_NAME = r"[a-zA-Z]+"
t_GREET = r"(greet)|(hello)|(howdy)"
t_EQUALS = r"\="
t_STACKASCII = r"stackascii"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_EXPO = r"\^"


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print(f"Integer value too large: {t.value}")
        t.value = 0
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character {t.value[0]!r} on line {t.lexer.lineno}")
    t.lexer.skip(1)

t_ignore = ' \t\n'

stack = []

lexer = lex.lex()

# Parsing

def p_expression_operators(t):
    '''
    expression : NUMBER ADD NUMBER
               | NUMBER SUBTRACT NUMBER
               | NUMBER MULTIPLY NUMBER
               | NUMBER DIVIDE NUMBER
               | NUMBER EXPO NUMBER
    '''
    if t[2] == "+":
        t[0] = t[1] + t[3]
    elif t[2] == "-":
        t[0] = t[1] - t[3]
    elif t[2] == "*":
        t[0] = t[1] * t[3]
    elif t[2] == "/":
        t[0] = t[1] / t[3]
    elif t[2] == "^":
        t[0] = t[1] ** t[3]

def p_greet(t):
    'expression : GREET LPAREN NAME RPAREN'
    mygreets = ["Hello","Howdy","Hello there","How are you"]
    r = random.choice(mygreets)
    print(f"{r}, {t[3]}!")

def p_pushstack(t):
    'expression : NAME LPAREN NUMBER RPAREN'
    if t[1] == "stack":
        stack.append(t[3])
        print(f"Pushed {t[3]} to stack")
    else:
        print(f"{t[1]} could not be identified")

def p_asciistack(t):
    'expression : STACKASCII LPAREN RPAREN'
    ret = ""
    for x in stack:
        ret = ret + chr(int(x))
    print(ret)

def p_error(t):
    if t is None: # lexer error
        return
    print(f"Syntax Error: {t.value!r}")

parser = yacc.yacc()

if __name__ == "__main__":
    with open('jaelang.txt') as tf:
        s = tf.readlines()
        for line in s:
           parsed = parser.parse(line)
           print(parsed)
    print(f"Stack: {stack}")
