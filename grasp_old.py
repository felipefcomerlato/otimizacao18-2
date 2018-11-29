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
import time


def construct(current_node, local_cost):
    global count_infact
    global size_global_visiteds
    global capacities_aux

    # Add o nodo atual na lista de visitados da solucao local
    if current_node != garage:
        visiteds.append(current_node)

    ## Se RETORNOU a garagem, finaliza a solucao local,
    ## atualiza a solucao global e retorna
    if garage in visiteds:
        local_solution = list(itertools.chain(*[[garage], copy.deepcopy(visiteds)])) #flattened list
        solution.append(copy.deepcopy(local_solution))
        size_global_visiteds += len(pre_global_visiteds)
        global_visiteds.append(list(itertools.chain(pre_global_visiteds)))
        # print("k="+str(garage)+" : "+str(local_solution)+" | Local cost: "+str(local_cost))
        costs_table.append(local_cost)
        del local_solution[:]
        capacities_aux[garage] = capacities_aux[garage] - 1
        count_infact = 0
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
            count_infact += 1
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
    ## e no "peso" baseado no tamanho do rcl do possivel candidato
    for c in candidates:
        if graph[current_node][c] <= limit:
            rcl.append(c)
            if c != garage:
                ####################################
                # Preve os candidatos do possivel destino
                future_candidates = []
                for dest in range(len(graph[c])):
                    if dest not in list(itertools.chain(*global_visiteds)):
                        if dest not in visiteds:
                            if graph[c][dest] != -1:
                                if dest > k_garages-1 or dest == garage:
                                    future_candidates.append(dest)
                # Preve os custos dos candidatos do possivel destino
                future_candidates_costs = []
                for f in future_candidates:
                    future_candidates_costs.append((f, graph[c][f]))
                # Preve o limitante dos candidatos do possivel destino
                future_max_s = max(future_candidates_costs,key=lambda item:item[1])[1]
                future_min_s = min(future_candidates_costs,key=lambda item:item[1])[1]
                future_limit = future_min_s + (alpha/2)*(future_max_s - future_min_s)
                # Insere o candidato X vezes no atual rcl,
                # onde X eh o tamanho do rcl do candidato
                for f in future_candidates:
                    if graph[c][f] <= future_limit:
                        rcl.append(c)
                ###################################

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

count_infact = 0
size_global_visiteds = 0
current_optimal_cost = -1

def run(graph_instance, garages_instance, capacities_instance, trips_instance):

    global solution, global_visiteds, garage, candidates, rcl, local_cost, visiteds
    global graph, alpha, k_garages, capacities, capacities_aux
    global pre_global_visiteds, costs_table, trips
    global size_global_visiteds, count_infact
    global current_optimal_cost

    graph = graph_instance
    k_garages = garages_instance
    capacities = capacities_instance
    trips = trips_instance


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
    total_vehicles = sum(capacities)

    print("\n######################################\n")
    # print(len(global_visiteds))
    # print(trips)
    initial_time = time.time()
    alpha_str = str(alpha).split(".")
    alpha_int = alpha_str[0]
    if len(alpha_str) > 1:
        alpha_dec = alpha_str[1]
    else:
        alpha_dec = "00"
    output_name = "output_files/output_grasp_"+alpha_int+"_"+alpha_dec+".txt"
    open(output_name, 'w').close()
    while True:
        if time.time() - initial_time > 3600:
            break
        capacities_aux = copy.deepcopy(capacities)
        del solution[:]
        while size_global_visiteds < trips:
            if count_infact < trips*k_garages*sum(capacities):
                garage = random.randrange(0,k_garages) # 0, ... k_garages-1
                local_cost = 0
                if capacities_aux[garage] > 0:
                    construct(garage,local_cost)
                del visiteds[:]
                del pre_global_visiteds[:]
            else:
                size_global_visiteds = trips

            if sum(capacities_aux) == 0 or (current_optimal_cost > 0 and sum(costs_table) >= current_optimal_cost):
                break
            # END INTERN WHILE

        global_visiteds = list(itertools.chain(*global_visiteds))

        total_cost = sum(costs_table)
        if current_optimal_cost != -1:
            if total_cost < current_optimal_cost:
                current_optimal_cost = total_cost
                file_writer(output_name, total_cost, solution, total_vehicles - sum(capacities_aux))
                print("\nTotal cost: "+str(total_cost))
                # print("Final solution: "+str(solution))
        else:
            current_optimal_cost = total_cost

        # print("Visited places: "+str(global_visiteds)+"\n")
        del global_visiteds[:]
        del costs_table[:]
        del visiteds[:]
        del pre_global_visiteds[:]
        size_global_visiteds = 0
        count_infact = 0

def file_writer(output_name, total_cost, solution, vehicles):
    file = open(output_name,"a")

    file.write("\nCusto: "+str(total_cost)+" | Veiculos: "+str(vehicles))
    file.write("\nSolucao: ")
    for sequence in solution:
        garage = sequence[0]
        file.write("\n(K="+str(garage)+") -> ")
        first = True
        for trip in sequence:
            if trip == garage:
                if not first:
                    file.write("(K="+str(garage)+")")
            else:
                file.write("(i="+str(trip)+") -> ")
            first = False
    file.write("\n")
    file.close()
