%module tinyxml2
%include cpointer.i
%pointer_functions(int, intp);
%{
#include "tinyxml2.h"
%}
%include tinyxml2.h