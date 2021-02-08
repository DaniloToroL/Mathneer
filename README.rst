*************************************************
mathneer -- Math API for engineering calculations
*************************************************

Introduction
************

API for engineering calculations with a simple syntax. 

Sintax
******

exponent   :: '^'

multiplication  :: '*' | '/'

add  :: '+' | '-'

integer :: ['+' | '-'] '0'..'9'+

atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'

factor  :: atom [ expop factor ]*

term    :: factor [ multop factor ]*

expr    :: term [ addop term ]*

To Do List
##########
1. Math calculations

  * Geometry
  * Calculus 
  * Algebra

2. API
3. Engineering problems

  * Thermodynamics
  * Material strength
  * Fluid Dynamics




