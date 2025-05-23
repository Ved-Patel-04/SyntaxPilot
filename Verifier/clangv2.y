%{
    #include <stdio.h>
    #include <stdlib.h>
    int yylex();
    void yyerror(const char *s);
%}
%token EQUAL IDENTIFIER SEMICOLON INT 
%token MULTIPLY DIVIDE PLUS MINUS MODULO
%token LPAREN RPAREN RBRACE LBRACE
%token FOR NUM WHILE DO
%token LT GT LE GE EQUALTO NOTEQUAL
%token INC DEC
%start translation-unit
%%
translation-unit
    : loop-statement {return 0;}
    | declaration {return 0;}
    | assignment {return 0;}
    | unary SEMICOLON {return 0;}
    ;

declaration
    : typename IDENTIFIER SEMICOLON
    ;

declaration-no-semi
    : typename IDENTIFIER 
    ;

assignment
    : typename IDENTIFIER EQUAL statement SEMICOLON
    | IDENTIFIER EQUAL statement SEMICOLON
    ;

assignment-no-semi
    : typename IDENTIFIER EQUAL statement 
    | IDENTIFIER EQUAL statement 
    ;

statement
    : NUM
    | statement PLUS statement
    | statement MINUS statement
    | statement MULTIPLY statement
    | statement DIVIDE statement
    | statement MODULO statement
    ;

typename
    : INT
    ;

loop-statement
    : for-loop
    | while-loop
    | do-while-loop
    ;

for-loop
    : FOR LPAREN expression-opt SEMICOLON expression-opt SEMICOLON expression-opt RPAREN statement SEMICOLON 
    ;

while-loop
    : WHILE LPAREN expression RPAREN statement
    ;

do-while-loop
    : DO statement WHILE LPAREN expression RPAREN SEMICOLON
    ;

expression-opt 
    : expression
    | %empty
    ;

expression
    : declaration-no-semi
    | assignment-no-semi
    | comparison
    | unary
    ;

comparison
    : IDENTIFIER LT ident-or-lit
    | IDENTIFIER GT ident-or-lit
    | IDENTIFIER GE ident-or-lit
    | IDENTIFIER LE ident-or-lit
    | IDENTIFIER NOTEQUAL ident-or-lit
    | IDENTIFIER EQUALTO ident-or-lit
    ;

ident-or-lit
    : IDENTIFIER
    | NUM
    ;

unary
    : IDENTIFIER INC
    | IDENTIFIER DEC
    ;
%%

int main(void) {
    int returnVal = 0;
    if (yyparse() != 0) {
        returnVal = 1;
    }
    return returnVal;
}
void yyerror(const char *s) {
    //fprintf(stderr, "Error: %s\n", s);
}
