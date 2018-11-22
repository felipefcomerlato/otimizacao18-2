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
#arco -> (u, v, custo)
# graph = [
#             [(4,1), (3,2), (2,4), (1,10)],
#             [(4,7), (3,6), (2,12), (0,10)],
#             [(1,12), (3,3), (0,4), (4,6)],
#             [(4,5), (0,2), (1,6), (2,3)],
#             [(0,1), (1,7), (2,6), (3,5)]
#         ]

# graph = [
#             [-1, -1, 5032, 5028, 5025, 5073],
#             [-1, -1, 5070, 5067, 5026, 5047],
#             [5023, 5019, -1, -1, 138, 248],
#             [5052, 5059, -1, -1, 332, 212],
#             [5061, 5062, -1, -1, -1, 84],
#             [5053, 5023, -1, -1, -1, -1]
#         ]

graph = [
            [-1, -1, 5032, 5028, 5025, 5073],
            [-1, -1, 5070, 5067, 5026, 5047],
            [5023, 5019, -1, -1, 138, 248],
            [5052, 5059, -1, -1, 332, 212],
            [5061, 5062, -1, -1, -1, 84],
            [5053, 5023, -1, -1, -1, -1]
        ]

# for nodo in range(len(graph)):
#     for arco in range(len(graph[nodo])):
#         if nodo == 1:
#             print(graph[nodo][arco][1]) # Printa todos candidates_costs de arcos ligados ao nodo 1
alpha = 0.2
solution = []
n_garages = 2

init_node = 0 # Garage K
candidates = [] #refresh for each trip inside sequence
rcl = [] #
local_cost = 0
visiteds = []

print("\nNodo inicial: " + str(init_node) + "\n")

def construct(current_node, local_cost):

    print("Nodo atual: " + str(current_node))

    ## Atualiza solucao local com o nodo atual
    if current_node != init_node:
        visiteds.append(current_node)

    if init_node in visiteds: # Se RETORNOU a garagem
        if len(visiteds) < 2:
            print("Nem saiu da garagem "+str(init_node))
            return 0
        local_solution = [init_node, visiteds]
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

#########################################################################
#####-----OS NODOS VISITADOS SAO CUMULATIVOS ATE PASSAR POR TODAS GARAGENS
#########################################################################

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
    # copia = copy.deepcopy(origem)

    print("candidates: " + str(candidates))
    print("Max: " + str(max_s) + " / Min: " + str(min_s) + " / Limit: " + str(limit))
    print("RCL: " + str(rcl) + " / Dest escolhido: " + str(rcl[choice]))
    print("\n--------\n")
    next_node = rcl[choice]
    if next_node == init_node:
        visiteds.append(init_node)
    del candidates[:]
    del rcl[:]
    construct(next_node, local_cost)

# print(max(candidates,key=itemgetter(1))[0])
construct(init_node, local_cost)
#...
