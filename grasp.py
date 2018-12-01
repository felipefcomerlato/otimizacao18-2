import copy
import itertools
import random
import time

solution = [] #FINAL
global_visiteds = [] #TODAS AS VIAGENS FEITAS
pre_global_visiteds = [] #construtor das viagens feitas (se infactivel ele eh zerado)
candidates = [] #CANDIDATOS DE CADA NODO
rcl = [] #RCL DE CADA NODO
visiteds = [] #INCLUI A GARAGEM
costs_table = [] #CUSTOS DE CADA SEQUENCIA DE VIAGENS

count_infact = 0
size_global_visiteds = 0
current_optimal_cost = -1
global_optimal_cost = float("inf")

graph = []
k_garages = 0
capacities = []
capacities_aux = [] #USADO NA CONSTRUCAO DE UMA SOLUCAO
trips = 0
total_vehicles = 0
alpha = 0
current_seed = 0

def setParams(graph_instance, k_garages_instance, capacities_instance, trips_instance):
    global graph, k_garages, capacities, trips, total_vehicles
    graph = graph_instance
    k_garages = k_garages_instance
    capacities = capacities_instance
    trips = trips_instance
    total_vehicles = sum(capacities)
    grasp()

def grasp():
    global alpha, current_seed, count_infact, global_visiteds
    global current_optimal_cost, global_optimal_cost
    alpha = getAlpha()
    output_file = setOutput(alpha)
    maxIt = 200
    print("\n######################\n")

    current_seed = random.randrange(0,999999)
    while True:
        if current_optimal_cost < global_optimal_cost:
            global_optimal_cost = current_optimal_cost
        random.seed(current_seed)
        current_seed += 1
        # for i in range(maxIt):
        del solution[:]
        initial_time = time.time()
        construct()
        # local(solution)
        solution_time = time.time() - initial_time

        global_visiteds = list(itertools.chain(*global_visiteds))
        total_cost = sum(costs_table)
        if current_optimal_cost != -1:
            if total_cost < current_optimal_cost and total_cost > 0:
                current_optimal_cost = total_cost
                file_writer(output_file, total_cost, solution, total_vehicles - sum(capacities_aux))
                print("Total cost: "+str(total_cost)+" | Vehicles: "+str(total_vehicles - sum(capacities_aux)))
                print("Seed: "+str(current_seed)+" | Time: "+str(solution_time*1000))
        else:
            file_writer(output_file, total_cost, solution, total_vehicles - sum(capacities_aux))
            print("\nInitial solution:")
            print("Total cost: "+str(total_cost)+" | Vehicles: "+str(total_vehicles - sum(capacities_aux)))
            print("Seed: "+str(current_seed)+" | Time: "+str(solution_time*1000)+"\n")
            current_optimal_cost = total_cost

        del global_visiteds[:]
        del costs_table[:]
        del visiteds[:]
        del pre_global_visiteds[:]
        size_global_visiteds = 0
        count_infact = 0

def construct():
    global count_infact, size_global_visiteds, current_optimal_cost
    global capacities_aux, global_visiteds

    capacities_aux = copy.deepcopy(capacities)

    while size_global_visiteds < trips:
        if count_infact < trips*k_garages*sum(capacities):
            garage = random.randrange(0,k_garages) # 0, ... k_garages-1
            local_cost = 0
            if capacities_aux[garage] > 0:
                ## Gera uma sequencia de viagens factivel
                generate_sequence(garage, garage, local_cost)
                capacities_aux[garage] = capacities_aux[garage] - 1
            del visiteds[:]
            del pre_global_visiteds[:]
        else:
            size_global_visiteds = trips

        if sum(capacities_aux) == 0 or (current_optimal_cost > 0 and sum(costs_table) >= current_optimal_cost):
            break
    size_global_visiteds = 0


def generate_sequence(current_node, garage, local_cost):
    global size_global_visiteds
    if current_node != garage:
        visiteds.append(current_node)

    if garage in visiteds: ## Encontrada uma sequencia de viagens factivel para um veiculo
        local_solution = list(itertools.chain(*[[garage], copy.deepcopy(visiteds)]))
        solution.append(copy.deepcopy(local_solution))
        size_global_visiteds += len(pre_global_visiteds)
        global_visiteds.append(list(itertools.chain(pre_global_visiteds)))
        costs_table.append(local_cost)
        del local_solution[:]
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

    next_node = rcl[choice]
    if next_node == garage:
        visiteds.append(garage)
    else:
        pre_global_visiteds.append(next_node)

    ## Limpa as listas locais
    del candidates[:]
    del rcl[:]
    del candidates_costs[:]
    ## Continua construindo a sequencia a partir do nodo destino
    generate_sequence(next_node, garage, local_cost)


def setOutput(alpha):
    alpha_str = str(alpha).split(".")
    alpha_int = alpha_str[0]
    if len(alpha_str) > 1:
        alpha_dec = alpha_str[1]
    else:
        alpha_dec = "00"
    output_name = "output_files/output_grasp_"+alpha_int+"_"+alpha_dec+".txt"
    open(output_name, 'w').close()
    return output_name


def getAlpha():
    alpha = float(raw_input("Alpha (entre 0.0 e 1.0): "))
    if alpha < 0.0 or alpha > 1.0:
        print("O valor de Alpha deve estar entre 0.0 e 1.0. Tente novamente")
        getAlpha()
    return alpha

def file_writer(output_file, total_cost, solution, vehicles):
    file = open(output_file,"a")
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
