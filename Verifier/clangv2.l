%{
#include <stdio.h>
#include <stdlib.h>
#include "clangv2.tab.h"
%}
%%
"=" return EQUAL;
"(" return LPAREN;
")" return RPAREN;
"{" return LBRACE;
"}" return RBRACE;
"*" return MULTIPLY;
"/" return DIVIDE;
"+" return PLUS;
"-" return MINUS;
"%" return MODULO;
";" return SEMICOLON;
"int" return INT;
"while" return WHILE;
"for" return FOR;
"do" return DO;
"<" return LT;
">" return GT;
">=" return GE;
"<=" return LE;
"==" return EQUALTO;
"!=" return NOTEQUAL;
"++" return INC;
"--" return DEC;
[0-9]+ return NUM;
[a-zA-Z_][a-zA-Z0-9_]* return IDENTIFIER;
[ \t]+ {}
%%
