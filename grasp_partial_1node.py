#########################################
#               GRASP
#########################################
# PSEUDOCODIGO:
# def grasp:
#     x* = infinito
#     for x = 1 to maxit do:
#         construct(g(), ALPHA, x)
#         local(f(),x)
#         if(f(x) < f(x*)):
#             x* = x
#
# def construct(g(),ALPHA,x):
#     x=0
#     inicializa candidatos C
#     while G != 0 do:
#         s_ = min { g(t)/tEC }
#         s- = max { g(t)/tEC }
#         RCL = { sEC/g(s) <= s_ + ALPHA*(s- - s_) }
#         select s at random from RCL
#         x = x U {s}
#         update candidatos C
import random
import copy
#arco -> (u, v, custo)
grafo = [[(5,1), (4,2), (3,4), (2,10)],[(5,7), (4,6), (3,12)],[(5,6), (4,3)],[(5,5)],[(-1,0)]]

# for nodo in range(len(grafo)):
#     for arco in range(len(grafo[nodo])):
#         if nodo == 1:
#             print(grafo[nodo][arco][1]) # Printa todos custos de arcos ligados ao nodo 1
alpha = 0.2
init_nodo = 0
current_nodo = init_nodo
candidatos = []
rcl = []
solution = []

for arco in grafo[current_nodo]:
    candidatos.append(arco)

max_s = max(candidatos,key=lambda item:item[1])[1]
min_s = min(candidatos,key=lambda item:item[1])[1]
limit = min_s + alpha*(max_s - min_s)

for c in candidatos:
    if c[1] <= limit:
        rcl.append(c)

choice = random.randrange(0,len(rcl))
solution.append((current_nodo,rcl[choice][0],rcl[choice][1]))
# copia = copy.deepcopy(origem)

print("Nodo atual: " + str(current_nodo))
print("Candidatos: " + str(candidatos))
print("Max: " + str(max_s))
print("Min: " + str(min_s))
print("Limitante: " + str(limit))
print("RCL: " + str(rcl))
print("Caminho escolhido: " + str(rcl[choice]))
print("Solucao ate o momento: " + str(solution))
print("Novo nodo atual: " + str(rcl[choice][0]))
print("\n--------\n")



# print(max(candidatos,key=itemgetter(1))[0])
























#...
