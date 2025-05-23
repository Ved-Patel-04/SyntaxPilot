#!/bin/bash
flex clangv2.l
bison -d clangv2.y
gcc -o verifier lex.yy.c clangv2.tab.c -lfl 
