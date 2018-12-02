/* glpsol --model -m mdvsp.mod --data input.dat -o cost.sol --tmlim 60  */

set V;
set K;
set T;

param C{k in K};
param COST{i in V, j in V};

var Xij{k in K, i in V, j in V} >= 0 binary;

minimize obj: sum {k in K} sum{i in V, j in V: COST[i,j] != -1} (COST[i,j] * Xij[k,i,j]);

s.t. R0{i in T}: sum{k in K, j in V: COST[i,j] != -1} Xij[k,i,j] == 1;

s.t. R1{k in K}: sum{j in T} Xij[k,k,j] <= C[k];

s.t. R2{k in K, i in T}: sum{j in V: COST[j,i] != -1} Xij[k,j,i] - sum{j in V: COST[i,j] != -1} Xij[k,i,j] == 0;
