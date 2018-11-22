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
#     inicializa candidates C
#     while G != 0 do:
#         s_ = min { g(t)/tEC }
#         s- = max { g(t)/tEC }
#         RCL = { sEC/g(s) <= s_ + ALPHA*(s- - s_) }
#         select s at random from RCL
#         x = x U {s}
#         update candidates C

import random
import copy
import itertools

graph = [
            [-1, -1, 5032, 5028, 5025, 5073],
            [-1, -1, 5070, 5067, 5026, 5047],
            [5023, 5019, -1, -1, 138, 248],
            [5052, 5059, -1, -1, 332, 212],
            [5061, 5062, -1, -1, -1, 84],
            [5053, 5023, -1, -1, -1, -1]
        ]

alpha = 0.2
solution = []
global_visiteds = []
n_garages = 2

init_node = 0 # Garage K
candidates = [] #refresh for each trip inside sequence
rcl = []
local_cost = 0
visiteds = []

def construct(current_node, local_cost):

    print("Nodo atual: " + str(current_node))

    ## Atualiza solucao local com o nodo atual
    if current_node != init_node:
        visiteds.append(current_node)

    ## Se RETORNOU a garagem, finaliza a solucao local,
    ## atualiza a solucao global e retorna
    if init_node in visiteds:
        local_solution = list(itertools.chain(*[[init_node], visiteds])) #flattened list
        solution.append(local_solution)
        # Custo total a partir da garagem k
        print("Solucao local (garagem "+str(init_node)+"): "+str(local_solution)+" | Custo local: "+str(local_cost))
        return 0

    ## Gera os candidates a partir do nodo atual
    ## A garagem (origem) sempre eh um candidato
    for dest in range(len(graph[current_node])):
        if dest not in visiteds:
            if graph[current_node][dest] != -1:
                if dest > 1 or dest == init_node:
                    candidates.append(dest)

    ## Para o algoritmo caso nao haja caminho factivel
    if len(candidates) == 0:
        print("Nenhum caminho possivel")
        return 0

    ## Obtem o custo de cada candidato
    candidates_costs = []
    for c in candidates:
        candidates_costs.append((c, graph[current_node][c]))

    ## Pega o maior e menor custo entre os candidates
    ## e calcula o limitante com base no fator alpha
    max_s = max(candidates_costs,key=lambda item:item[1])[1]
    min_s = min(candidates_costs,key=lambda item:item[1])[1]
    limit = min_s + alpha*(max_s - min_s)

    ## Gera o RCL com base nos candidatos de custo abaixo do limitante
    for c in candidates:
        if graph[current_node][c] <= limit:
            rcl.append(c)

    ## Escolhe um caminho a seguir aleatoriamente dentre o contidos em RCL
    choice = random.randrange(0,len(rcl))
    local_cost = local_cost + graph[current_node][rcl[choice]]

    print("Candidatos: " + str(candidates))
    print("Max: " + str(max_s) + " / Min: " + str(min_s) + " / Limit: " + str(limit))
    print("RCL: " + str(rcl) + " / Dest escolhido: " + str(rcl[choice]))
    print("\n--------\n")

    ## Se o destino escolhido for a garagem de partida,
    ## add a garagem como visitado para que na proxima iteracao o algoritmo
    ## saiba que deve retornar.
    ## Caso contrario, segue o fluxo normal, atualizando a lista global de visitados
    next_node = rcl[choice]
    if next_node == init_node:
        visiteds.append(init_node)
    else:
        global_visiteds.append(next_node)

    ## Limpa as listas locais
    del candidates[:]
    del rcl[:]
    del candidates_costs[:]

    ## Invoca contruct para o nodo destino
    construct(next_node, local_cost)

## end construct


construct(init_node, local_cost)

print("Viagens realizadas: "+str(global_visiteds))
