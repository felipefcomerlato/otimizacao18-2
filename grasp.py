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

import copy
import itertools
import random


def construct(current_node, local_cost):
    # print("garage:" + str(garage))
    ## Atualiza solucao local com o nodo atual
    if current_node != garage:
        visiteds.append(current_node)

    ## Se RETORNOU a garagem, finaliza a solucao local,
    ## atualiza a solucao global e retorna
    if garage in visiteds:
        local_solution = list(itertools.chain(*[[garage], copy.deepcopy(visiteds)])) #flattened list
        solution.append(copy.deepcopy(local_solution))
        global_visiteds.append(list(itertools.chain(pre_global_visiteds)))
        print("k="+str(garage)+" : "+str(local_solution)+" | Local cost: "+str(local_cost))
        costs_table.append(local_cost)
        del local_solution[:]
        capacities[garage] = capacities[garage] - 1
        return 1

    ## Gera os candidates a partir do nodo atual
    ## A garagem (origem) sempre eh um candidato
    for dest in range(len(graph[current_node])):
        if dest not in list(itertools.chain(*global_visiteds)):
            if dest not in visiteds:
                if graph[current_node][dest] != -1:
                    if dest > k_garages-1 or dest == garage:
                        candidates.append(dest)

    ## Retorna do algoritmo caso nao haja caminho factivel
    if len(candidates) == 0:
        if graph[current_node][garage] != -1:
            candidates.append(garage)
        else:
            print("k="+str(garage)+" : Impossible to return to the garage")
            garage_control[0] = 2
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

    # print("\nNodo atual: " + str(current_node))
    # print("Candidatos: " + str(candidates))
    # print("Max: " + str(max_s) + " / Min: " + str(min_s) + " / Limit: " + str(limit))
    # print("RCL: " + str(rcl) + " / Dest escolhido: " + str(rcl[choice]))

    ## Se o destino escolhido for a garagem de partida,
    ## add a garagem como visitado para que na proxima iteracao o algoritmo
    ## saiba que deve retornar.
    ## Caso contrario, segue o fluxo normal, atualizando a lista global de visitados
    next_node = rcl[choice]
    if next_node == garage:
        visiteds.append(garage)
    else:
        pre_global_visiteds.append(next_node)

    ## Limpa as listas locais
    del candidates[:]
    del rcl[:]
    del candidates_costs[:]

    ## Invoca contruct para o nodo destino
    construct(next_node, local_cost)

## end construct

def run(graph_instance, garages_instance, capacities_instance):

    global solution, global_visiteds, garage, candidates, rcl, local_cost, visiteds
    global graph, alpha, k_garages, capacities
    global pre_global_visiteds, costs_table

    graph = graph_instance
    k_garages = garages_instance
    capacities = capacities_instance

    def getAlpha():
        alpha = float(raw_input("Alpha (entre 0.0 e 1.0): "))
        if alpha < 0.0 or alpha > 1.0:
            print("O valor de Alpha deve estar entre 0.0 e 1.0. Tente novamente")
            getAlpha()
        return alpha

    alpha = getAlpha()
    solution = []
    global_visiteds = []
    pre_global_visiteds = []
    candidates = [] #refresh for each trip inside sequence
    rcl = []
    visiteds = []
    costs_table = []

    print("\n######################################\n")
    for k in range(k_garages): ## AQUI VAI UM WHILE (enquanto nao forem visitados todos os locais)
        garage = random.randrange(0,k_garages) # 0, ... k_garages-1
        local_cost = 0
        del visiteds[:]
        del pre_global_visiteds[:]
        if capacities[garage] > 0: ## SE AINDA TEM BUS DISPONIVEL
            construct(garage,local_cost)

        # print("Garage: "+str(garage)+" -> "+str(capacities[garage]))
        # capacities[garage] = capacities[garage] - 1

    global_visiteds = list(itertools.chain(*global_visiteds))

    print("\nFinal solution: "+str(solution))
    print("Total cost: "+str(sum(costs_table)))
    print("Visited places: "+str(global_visiteds)+"\n")
    print("Capacities: "+str(capacities))

# construct(garage, local_cost)

# print("Viagens realizadas: "+str(global_visiteds))
