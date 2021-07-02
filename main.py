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
    'EXPO',
    'STRING',
    'GETSTACK'
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
t_STRING = r"\"(.*?)\""
t_GETSTACK = r"(getstack)|(gs)"


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
variables = {}

lexer = lex.lex()

# Parsing

def p_expression_operators(t):
    '''
    expression : NUMBER ADD NUMBER
               | NUMBER SUBTRACT NUMBER
               | NUMBER MULTIPLY NUMBER
               | NUMBER DIVIDE NUMBER
               | NUMBER EXPO NUMBER
               | NAME ADD NUMBER
               | NAME SUBTRACT NUMBER
               | NAME MULTIPLY NUMBER
               | NAME DIVIDE NUMBER
               | NAME EXPO NUMBER
               | NUMBER ADD NAME
               | NUMBER SUBTRACT NAME
               | NUMBER MULTIPLY NAME
               | NUMBER DIVIDE NAME
               | NUMBER EXPO NAME
               | NAME ADD NAME
               | NAME SUBTRACT NAME
               | NAME MULTIPLY NAME
               | NAME DIVIDE NAME
               | NAME EXPO NAME
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
    '''
    expression : NAME LPAREN NUMBER RPAREN
               | NAME LPAREN STRING LPAREN RPAREN RPAREN
    '''
    if t[1] == "stack":
        stack.append(t[3])
    else:
        print(f"{t[1]} could not be identified")

def p_asciistack(t):
    'expression : STACKASCII LPAREN RPAREN'
    ret = ""
    for x in stack:
        ret = ret + chr(int(x))
    print(ret)

def p_getstack(t):
    '''
    expression : GETSTACK LPAREN NUMBER RPAREN
               | GETSTACK LPAREN STRING RPAREN
    '''
    if isinstance(t[3],int):
        t[0] = stack[int(t[3])]
    elif isinstance(t[3],str):
        t[0] = [s for s in stack if t[3] == s]

def p_declarevariable(t):
    '''
    expression : NAME EQUALS NUMBER
               | NAME EQUALS STRING
    '''
    if str(t[1]) in variables:
        variables[str(t[1])] = t[3]
    else:
        variables[t[1]] = t[3]

def p_usevariable(t):
    '''
    expression : NAME
    '''
    if str(t[1]) in variables:
        t[0] = variables[str(t[1])]
    else:
        print(f"Error: variable '{t[1]}' does not exist in the current context")

def p_error(t):
    if t is None: # lexer error
        print(f"Syntax Error: NONETYPE")
        return
    print(f"Syntax Error: {t.value!r}")

parser = yacc.yacc()

lines = 0

if __name__ == "__main__":
    with open('jaelang.txt') as tf:
        s = tf.readlines()
        for line in s:
           lines = lines + 1
           parsed = parser.parse(line)
           if parsed != None:
            print(f"Line {str(lines)}: {parsed}")
    print("\n\n")
    print(" The program has finished")
    print(f"Stack: {stack}")
    print(f"Variables: {variables}")
