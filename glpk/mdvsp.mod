/* glpsol --model -m mdvsp.mod --data input.dat -o cost.sol --tmlim 60  */

set V;
set K;
set T;

param C{k in K};
param COST{i in V, j in V};

var Xij{i in V, j in V} >= 0 binary;

minimize obj: sum{i in V, j in V} (COST[i,j] * Xij[i,j]);

s.t. R0{i in T}: sum{j in V}(Xij[i,j]) = 1;
s.t. R1{k in K}: sum{j in T}(Xij[k,j]) <= C[k];
s.t. R2{i in V}: (sum{j in V}(Xij[i,j]) - sum{j in V}(Xij[j,i])) = 0;
s.t. R3{i in V, j in V}: COST[i,j]*Xij[i,j] >= 0;
