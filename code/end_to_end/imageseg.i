%module imageseg
%include cpointer.i
%include "std_vector.i"
%pointer_functions(int, intp);
namespace std{
	%template(vectori) vector<rect>;
	%template(vectorb) vector<pattern>;
	%template(vectorf1) vector<block>;
	%template(vectorf2) vector<int>;
	%template(vectorf3) vector<float>;
};
%{
#include "imageseg.h"
%}
%include imageseg.h