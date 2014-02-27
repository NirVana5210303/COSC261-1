import re
import sys

# Restrictions:
# Integer constants must be short.
# Stack size must not exceed 1024.
# Integer is the only type.
# Logical operators cannot be nested.

class Scanner:
    '''The interface comprises the methods lookahead and consume.
       Other methods should not be called from outside of this class.'''

    def __init__(self, input_file):
        '''Reads the whole input_file to input_string.'''
        # source code of the program to be compiled
        self.input_string = input_file.read()
        # index where the unprocessed part of input_string starts
        self.current_char_index = 0
        # a pair (most recently read token, matched substring of input_string)
        self.current_token = self.get_token()

    def skip_white_space(self):
        '''Consumes all characters in input_string up to the next
           non-white-space character.'''
        while self.current_char_index < len(self.input_string):
            if self.input_string[self.current_char_index].isspace() == True:
                self.current_char_index += 1
            else:
                break
        
    def get_token(self):
        '''Returns the next token and the part of input_string it matched.
           Returns None if there is no next token.
           The characters up to the end of the token are consumed.'''
        self.skip_white_space()
        # find the longest prefix of input_string that matches a token
        token, longest = None, ''
        for (t, r) in Token.token_regexp:
            match = re.match(r, self.input_string[self.current_char_index:])
            if match and match.end() > len(longest):
                token, longest = t, match.group()
        # consume the token by moving the index to the end of the matched part
        self.current_char_index += len(longest)
        return (token, longest)

    def lookahead(self):
        '''Returns the next token without consuming it.
           Returns None if there is no next token.'''
        return self.current_token[0]

    def consume(self, *tokens):
        '''Returns the next token and consumes it, if it is in tokens.
           Raises an exception otherwise.
           If the token is a number or an identifier, its value is returned.'''
        if self.current_token[0] in tokens:
            if (self.current_token[0] is Token.ID) or (self.current_token[0] is Token.NUM):
                s = self.current_token[1]
                self.current_token = self.get_token()
                return s
            else:
                s = self.current_token[0]
                self.current_token = self.get_token()
                return s
        else:
            raise Exception('The token isnt in the token list')
        
class Token:
    DO    = 'DO';
    ELSE  = 'ELSE';
    AND   = 'AND'    #Q8
    OR    = 'OR';
    NOT   = 'NOT';
    END   = 'END';
    IF    = 'IF';
    THEN  = 'THEN';
    WHILE = 'WHILE';
    SEM   = 'SEM';
    BEC   = 'BEC';
    LESS  = 'LESS';
    EQ    = 'EQ';
    GRTR  = 'GRTR';
    LEQ   = 'LEQ';
    NEQ   = 'NEQ';
    GEQ   = 'GEQ';
    ADD   = 'ADD';
    SUB   = 'SUB';
    MUL   = 'MUL';
    DIV   = 'DIV';
    LPAR  = 'LPAR';
    RPAR  = 'RPAR';
    NUM   = 'NUM';
    READ  = 'READ';
    WRITE = 'WRITE';
    ID    = 'ID';

    # The following list gives the regular expression to match a token.
    # The order in the list matters for mimicking Flex behaviour.
    # Longer matches are preferred over shorter ones.
    # For same-length matches, the first in the list is preferred.
    token_regexp = [
        (DO,    'do'),
        (ELSE,  'else'),
        (AND,   'and'),  #  Q8
        (OR,    'or'),    #  Boolean expression
        (NOT,   'not'),
        (END,   'end'),
        (IF,    'if'),
        (THEN,  'then'),
        (WHILE, 'while'),
        (WRITE, 'write'), # add read & write
        (READ,  'read'),
        (SEM,   ';'),
        (BEC,   ':='),
        (LESS,  '<'),
        (EQ,    '='),
        (GRTR,  '>'),
        (NEQ,   '!='),
        (LEQ,   '<='),
        (GEQ,   '>='),
        (ADD,   '[+]'), # + is special in regular expressions
        (SUB,   '-'),
        (MUL,   '[*]'),   #Multiplication in regular expressions
        (DIV,   '[/]'),   #Division in regular expressions
        (LPAR,  '[(]'), # ( is special in regular expressions
        (RPAR,  '[)]'), # ) is special in regular expressions
        (NUM,   '[0-9]+'),
        (ID,    '[a-z]+'),
    ]

class Symbol_Table:
    '''A symbol table maps identifiers to locations.'''
    def __init__(self):
        self.symbol_table = {}
    def size(self):
        '''Returns the number of entries in the symbol table.'''
        return len(self.symbol_table)
    def location(self, identifier):
        '''Returns the location of an identifier. If the identifier is not in
           the symbol table, it is entered with a new location. Locations are
           numbered sequentially starting with 0.'''
        if identifier in self.symbol_table:
            return self.symbol_table[identifier]
        index = len(self.symbol_table)
        self.symbol_table[identifier] = index
        return index

class Label:
    def __init__(self):
        self.current_label = 0
    def next(self):
        '''Returns a new, unique label.'''
        self.current_label += 1
        return 'l' + str(self.current_label)

def indent(s, level):
    return '    '*level + s + '\n'

# Each of the following classes is a kind of node in the abstract syntax tree.
# indented(level) returns a string that shows the tree levels by indentation.
# code() returns a string with JVM bytecode implementing the tree fragment.
# true_code/false_code(label) jumps to label if the condition is/is not true.
# Execution of the generated code leaves the value of expressions on the stack.

class Program_AST:
    def __init__(self, program):
        self.program = program
    def __repr__(self):
        return repr(self.program)
    def indented(self, level):
        return self.program.indented(level)
    def code(self):
        program = self.program.code()
        local = symbol_table.size()
        java_scanner = symbol_table.location('Java Scanner')
        return '.class public Program\n' + \
               '.super java/lang/Object\n' + \
               '.method public <init>()V\n' + \
               'aload_0\n' + \
               'invokenonvirtual java/lang/Object/<init>()V\n' + \
               'return\n' + \
               '.end method\n' + \
               '.method public static main([Ljava/lang/String;)V\n' + \
               '.limit locals ' + str(local) + '\n' + \
               '.limit stack 1024\n' + \
               'new java/util/Scanner\n' + \
               'dup\n' + \
               'getstatic java/lang/System.in Ljava/io/InputStream;\n' + \
               'invokespecial java/util/Scanner.<init>(Ljava/io/InputStream;)V\n' + \
               'astore ' + str(java_scanner) + '\n' + \
               program + \
               'return\n' + \
               '.end method\n'

class Statements_AST:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        result = repr(self.statements[0])
        for st in self.statements[1:]:
            result += '; ' + repr(st)
        return result
    def indented(self, level):
        result = indent('Statement(s)', level)
        for st in self.statements:
            result += st.indented(level+1)
        return result
    def code(self):
        result = ''
        for st in self.statements:
            result += st.code()
        return result

class If_AST:
    def __init__(self, condition, then):
        self.condition = condition
        self.then = then
    def __repr__(self):
        return 'if ' + repr(self.condition) + ' then ' + \
				       repr(self.then) + ' end'
				       
    def indented(self, level):
        return indent('If-Then', level) + \
               self.condition.indented(level+1) + \
               self.then.indented(level+1)
    def code(self):
        l1 = label_generator.next()
        return self.condition.false_code(l1) + \
               self.then.code() + \
               l1 + ':\n'
    
class If_Else_AST:   
    def __init__(self, condition, then, Else):
        self.condition = condition
        self.then = then
        self.Else = Else
    def __repr__(self):
        return 'if ' + repr(self.condition) + ' then ' + repr(self.then) + ' else ' + \
                       repr(self.Else) + ' end'
    
    def indented(self, level):
        return indent('If-Then-Else', level) + \
         self.condition.indented(level+1) + \
               self.then.indented(level+1) + \
               self.Else.indented(level+1)

    def code(self):
        l1 = label_generator.next()
        l2 = label_generator.next()
        
        return self.condition.false_code(l1) + \
               self.then.code() + \
               'goto ' + l2 + '\n' +\
               l1 + ':\n' + \
               self.Else.code() + \
               l2 + ':\n'    

class While_AST:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return 'while ' + repr(self.condition) + ' do ' + \
                          repr(self.body) + ' end'
    def indented(self, llableevel):
        return indent('While-Do', level) + \
               self.condition.indented(level+1) + \
               self.body.indented(level+1)
    def code(self):
        l1 = label_generator.next()
        l2 = label_generator.next()
        return l1 + ':\n' + \
               self.condition.false_code(l2) + \
               self.body.code() + \
               'goto ' + l1 + '\n' + \
               l2 + ':\n'

class Assign_AST:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
    def __repr__(self):
        return repr(self.identifier) + ':=' + repr(self.expression)
    def indented(self, level):
        return indent('Assign', level) + \
               self.identifier.indented(level+1) + \
               self.expression.indented(level+1)
    def code(self):
        loc = symbol_table.location(self.identifier.identifier)
        return self.expression.code() + \
               'istore ' + str(loc) + '\n'

class Write_AST:
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return 'write ' + repr(self.expression)
    def indented(self, level):
        return indent('Write', level) + self.expression.indented(level+1)
    def code(self):
        return 'getstatic java/lang/System/out Ljava/io/PrintStream;\n' + \
               self.expression.code() + \
               'invokestatic java/lang/String/valueOf(I)Ljava/lang/String;\n' + \
               'invokevirtual java/io/PrintStream/println(Ljava/lang/String;)V\n'
    
class Read_AST:
    def __init__(self, identifier):
        self.identifier = identifier
    def __repr__(self):
        return 'read ' + repr(self.identifier)
    def indented(self, level):
        return indent('Read', level) + self.identifier.indented(level+1)
    def code(self):
        java_scanner = symbol_table.location('Java Scanner')
        loc = symbol_table.location(self.identifier.identifier)
        return 'aload ' + str(java_scanner) + '\n' + \
               'invokevirtual java/util/Scanner.nextInt()I\n' + \
               'istore ' + str(loc) + '\n'

class Comparison_AST:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        op = { Token.LESS:'<', Token.EQ:'=', Token.GRTR:'>',
               Token.LEQ:'<=', Token.NEQ:'!=', Token.GEQ:'>=' }
        return repr(self.left) + op[self.op] + repr(self.right)
    def indented(self, level):
        return indent(self.op, level) + \
               self.left.indented(level+1) + \
               self.right.indented(level+1)
    def true_code(self, label):
        op = { Token.LESS:'if_icmplt', Token.EQ:'if_icmpeq',
               Token.GRTR:'if_icmpgt', Token.LEQ:'if_icmple',
               Token.NEQ:'if_icmpne', Token.GEQ:'if_icmpge' }
        return self.left.code() + \
               self.right.code() + \
               op[self.op] + ' ' + label + '\n'
    def false_code(self, label):
        # Negate each comparison because of jump to "false" label.
        op = { Token.LESS:'if_icmpge', Token.EQ:'if_icmpne',
               Token.GRTR:'if_icmple', Token.LEQ:'if_icmpgt',
               Token.NEQ:'if_icmpeq', Token.GEQ:'if_icmplt' }
        return self.left.code() + \
               self.right.code() + \
               op[self.op] + ' ' + label + '\n'
    
    
class Boolean_AST:   #Q8 boolean expression
    def __init__(self, left, op, right = None):
        self.left = left
        self.op = op
        self.right = right
        
    def __repr__(self):
        op = { Token.AND, Token.OR, Token.NOT }
        return repr(self.left) + self.op + repr(self.right)      
    
    def indented(self, level):
        if self.right != None:
            return indent(self.op, level) + \
               self.left.indented(level+1) + \
               self.right.indented(level+1)
        
        if self.right == None:
            return indent(self.op, level) + \
                   self.left.indented(level+1)
           
    def true_code(self, label):
        l1 = label_generator.next()
        op = { Token.AND, Token.OR, Token.NOT }
        if self.op == Token.OR:
            return self.left.true_code(label) + \
                   self.right.true_code(label) 
        if self.op == Token.AND:
            return self.left.false_code(l1) + \
                   self.right.true_code(label) + \
                   l1 + ':\n'
        if self.op == Token.NOT:
            return self.left.false_code(label)

    
    def false_code(self, label):
        l1 = label_generator.next()
        op = { Token.AND, Token.OR, Token.NOT }
        if self.op == Token.OR:
            return self.left.true_code(l1) + \
                   self.right.false_code(label) + \
                   l1 + ':\n'
        if self.op == Token.AND:
            return self.left.false_code(label) + \
                   self.right.false_code(label)
                   
        if self.op == Token.NOT:
            return self.left.true_code(label)
        

class Expression_AST:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        op = { Token.ADD:'+', Token.SUB:'-', Token.MUL:'*', Token.DIV:'/' }
        return '(' + repr(self.left) + op[self.op] + repr(self.right) + ')'
    def indented(self, level):
        return indent(self.op, level) + \
               self.left.indented(level+1) + \
               self.right.indented(level+1)
    def code(self):
        op = { Token.ADD:'iadd', Token.SUB:'isub',
               Token.MUL:'imul', Token.DIV:'idiv' }
        return self.left.code() + \
               self.right.code() + \
               op[self.op] + '\n'

class Number_AST:
    def __init__(self, number):
        self.number = number
    def __repr__(self):
        return self.number
    def indented(self, level):
        return indent(self.number, level)
    def code(self): # works only for short numbers
        return 'sipush ' + self.number + '\n'

class Identifier_AST:
    def __init__(self, identifier):
        self.identifier = identifier
    def __repr__(self):
        return self.identifier
    def indented(self, level):
        return indent(self.identifier, level)
    def code(self):
        loc = symbol_table.location(self.identifier)
        return 'iload ' + str(loc) + '\n'  
    def true_code(self, label):
        op = { Token.LESS:'if_icmplt', Token.EQ:'if_icmpeq',
               Token.GRTR:'if_icmpgt', Token.LEQ:'if_icmple',
               Token.NEQ:'if_icmpne', Token.GEQ:'if_icmpge' }
        return self.left.code() + \
               self.right.code() + \
               op[self.op] + ' ' + label + '\n'
    
    def false_code(self, label):
        # Negate each comparison because of jump to "false" label.
        op = { Token.LESS:'if_icmpge', Token.EQ:'if_icmpne',
               Token.GRTR:'if_icmple', Token.LEQ:'if_icmpgt',
               Token.NEQ:'if_icmpeq', Token.GEQ:'if_icmplt' }
        return self.left.code() + \
               self.right.code() + \
               op[self.op] + ' ' + label + '\n'



# The followingElse methods comprise the recursive-descent parser.

def program():
    sts = statements()
    return Program_AST(sts)

def statements():
    result = [statement()]
    while scanner.lookahead() == Token.SEM:
        scanner.consume(Token.SEM)
        st = statement()
        result.append(st)
    return Statements_AST(result)

def statement():
    if scanner.lookahead() == Token.IF:
        return if_statement()
    elif scanner.lookahead() == Token.WHILE:
        return while_statement()
    elif scanner.lookahead() == Token.ID:
        return assignment()
    elif scanner.lookahead() == Token.READ:
        return read()
    elif scanner.lookahead() == Token.WRITE:
        return write()
    else: # error
        return scanner.consume(Token.IF, Token.WHILE, Token.ID)

def if_statement():
    scanner.consume(Token.IF)
    condition = BooleanExpression()
    scanner.consume(Token.THEN)
    then = statements()

    
    if scanner.lookahead() ==  (Token.END):
        scanner.consume(Token.END)
        return If_AST(condition, then)
    elif scanner.lookahead() == (Token.ELSE):
        scanner.consume(Token.ELSE)
        Else = statements()
        scanner.consume(Token.END)
        return If_Else_AST(condition, then, Else)
    else:
        return scanner.consume(Token.END, Token.ELSE)

def read():  #Q6 Recursive read function
    scanner.consume(Token.READ)
    condition = identifier()
    return Read_AST(condition)

def write():     # Q5 Recursive write funciton
    scanner.consume(Token.WRITE)
    condition = expression()
    return Write_AST(condition)

def while_statement():
    scanner.consume(Token.WHILE)
    condition = BooleanExpression()
    scanner.consume(Token.DO)
    body = statements()
    scanner.consume(Token.END)

    return While_AST(condition, body)

def assignment():
    ident = identifier()
    scanner.consume(Token.BEC)
    expr = expression()
    return Assign_AST(ident, expr)

def comparison():
    left = expression()
    op = scanner.consume(Token.LESS, Token.EQ, Token.GRTR,
                         Token.LEQ, Token.NEQ, Token.GEQ)
    right = expression()
    return Comparison_AST(left, op, right)

def expression():
    result = term()
    while scanner.lookahead() in [Token.ADD, Token.SUB]:
        op = scanner.consume(Token.ADD, Token.SUB)
        tree = term()
        result = Expression_AST(result, op, tree)
    return result

def term():
    result = factor()
    while scanner.lookahead() in [Token.MUL, Token.DIV]:
        op = scanner.consume(Token.MUL, Token.DIV)
        tree = factor()
        result = Expression_AST(result, op, tree)
    return result

def factor():
    if scanner.lookahead() == Token.LPAR:
        scanner.consume(Token.LPAR)
        result = expression()
        scanner.consume(Token.RPAR)
        return result
    elif scanner.lookahead() == Token.NUM:
        value = scanner.consume(Token.NUM)
        return Number_AST(value)
    elif scanner.lookahead() == Token.ID:
        return identifier()
    else: # error
        return scanner.consume(Token.LPAR, Token.NUM, Token.ID)
    
def BooleanExpression():
    result = BooleanTerm()
    while scanner.lookahead() in [Token.AND]:
        op = scanner.consume(Token.AND)
        tree = BooleanTerm()
        result = Boolean_AST(tree, op, result)
    return result    
    
def BooleanTerm():
    result = BooleanFactor()
    while scanner.lookahead() in [Token.OR]:
        op = scanner.consume(Token.OR)
        tree = BooleanFactor()
        result = Boolean_AST(tree, op, result)
    return result
    
    
def BooleanFactor():
    if  scanner.lookahead() in [Token.NOT]:
        op = scanner.consume(Token.NOT)
        result = BooleanFactor()
        
    else:
        result = comparison()
    return result

def identifier():
    value = scanner.consume(Token.ID)
    return Identifier_AST(value)

# Initialise scanner, symbol table and label generator.
scanner = Scanner(sys.stdin)
symbol_table = Symbol_Table()
symbol_table.location('Java Scanner') # fix a location for the Java Scanner
label_generator = Label()

# Uncomment the following to test the scanner without the parser.
# This shows a list of all tokens in the input.
#
#token = scanner.lookahead()
#while token != None:
    #print(token)
    #scanner.consume(token)
    #token = scanner.lookahead()
#exit()

# Call the parser.

ast = program()
assert scanner.lookahead() == None

# Uncomment the following to test the parser without the code generator.
# The first line gives back the program by calling __repr__ of the AST classes.
# The second line shows the syntax tree with levels indicated by indentation.
#
#print(ast)
#print(ast.indented(0))
#exit()

# Call the code generator.

# This translates the abstract syntax tree to JVM bytecode.
# It can be assembled to a class file by Jasmin: http://jasmin.sourceforge.net/

print(ast.code())
