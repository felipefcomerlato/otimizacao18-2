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
grafo = [
            [(4,1), (3,2), (2,4), (1,10)],
            [(4,7), (3,6), (2,12), (0,10)],
            [(1,12), (3,3), (0,4), (4,6)],
            [(4,5), (0,2), (1,6), (2,3)],
            [(0,1), (1,7), (2,6), (3,5)]
        ]

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
visiteds = []

def construct(current_nodo):
    for arco in grafo[current_nodo]:
        if arco[0] == 0:
            finally_arco = arco
        elif arco[0] not in visiteds:
            candidatos.append(arco)

    visiteds.append(current_nodo)

    if len(candidatos) == 0:
        candidatos.append(finally_arco)
        solution.append((current_nodo,candidatos[0][0],candidatos[0][1]))
        print("Solucao final: "+str(solution))
        return 0

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
    current_nodo = rcl[choice][0]
    del candidatos[:]
    del rcl[:]
    construct(current_nodo)

# print(max(candidatos,key=itemgetter(1))[0])
construct(current_nodo)























#...
