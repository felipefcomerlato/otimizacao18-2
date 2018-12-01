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
initial_time = 0

def setParams(graph_instance, k_garages_instance, capacities_instance, trips_instance, input_file_name):
    global graph, k_garages, capacities, trips, total_vehicles
    graph = graph_instance
    k_garages = k_garages_instance
    capacities = capacities_instance
    trips = trips_instance
    total_vehicles = sum(capacities)
    grasp(input_file_name)

def grasp(input_file_name):
    global alpha, current_seed, count_infact, global_visiteds, initial_time
    global current_optimal_cost, global_optimal_cost
    alpha = getAlpha()
    output_file = setOutput(alpha, input_file_name)
    print("\n######################\n")
    initial_time = time.time()
    while True:
        current_seed = random.randrange(0,999999)
        random.seed(current_seed)
        current_seed += 1
        # for i in range(maxIt):
        del solution[:]
        current_optimal_cost = -1

        total_cost = 0
        construct()
        current_time = time.time() - initial_time

        total_cost = sum(costs_table)
        current_optimal_cost = total_cost
        global_visiteds = list(itertools.chain(*global_visiteds))

        # if current_optimal_cost != -1:
        #     if total_cost < current_optimal_cost and total_cost > 0:
        #         current_optimal_cost = total_cost
        #         file_writer(output_file, total_cost, solution, total_vehicles - sum(capacities_aux))
        #         print("Total cost: "+str(total_cost)+" | Vehicles: "+str(total_vehicles - sum(capacities_aux)))
        #         print("Seed: "+str(current_seed-1)+" | Time: "+str(solution_time*1000))
        # else:
        if current_optimal_cost < global_optimal_cost:
            file_writer(output_file, total_cost, solution, total_vehicles - sum(capacities_aux), current_seed-1, current_time)
            print("\nNew solution:")
            print("Total cost: "+str(total_cost)+" | Vehicles: "+str(total_vehicles - sum(capacities_aux)))
            print("Seed: "+str(current_seed-1)+" | Time(s): "+str("{0:.2f}".format(current_time))+"\n")
            current_optimal_cost = total_cost

        del global_visiteds[:]
        del costs_table[:]
        del visiteds[:]
        del pre_global_visiteds[:]
        size_global_visiteds = 0
        count_infact = 0

        while True:
            before = current_optimal_cost
            for seq in range(len(solution)):
                for i in range(1,len(solution[seq])-1):
                    local(seq, i)
                    current_time = time.time() - initial_time
                    if current_optimal_cost < global_optimal_cost:
                        global_optimal_cost = current_optimal_cost
                        file_writer(output_file, global_optimal_cost, solution, total_vehicles - sum(capacities_aux), current_seed-1, current_time)
                        # print("Total cost: "+str(total_cost)+" | Vehicles: "+str(total_vehicles - sum(capacities_aux)))
                        # print("Seed: "+str(current_seed-1)+" | Time: "+str(solution_time*1000)+"\n")
                        # print("Novo custo otimo: "+str(global_optimal_cost))
            if before == current_optimal_cost:
                break


def construct():
    global count_infact, size_global_visiteds, current_optimal_cost
    global capacities_aux, global_visiteds

    capacities_aux = copy.deepcopy(capacities)
    count_infact = 0
    size_global_visiteds = 0

    while size_global_visiteds < trips:
        # print(size_global_visiteds)
        if count_infact < trips*k_garages*sum(capacities):
            garage = random.randrange(0,k_garages)
            local_cost = 0
            if capacities_aux[garage] > 0:
                ## Gera uma sequencia de viagens factivel
                generate_sequence(garage, garage, local_cost)
                capacities_aux[garage] = capacities_aux[garage] - 1
            del visiteds[:]
            del pre_global_visiteds[:]
        else:
            del global_visiteds[:]
            del costs_table[:]
            del visiteds[:]
            del pre_global_visiteds[:]
            construct()

        if sum(capacities_aux) == 0:
            if size_global_visiteds == trips:
                break
            else:
                del global_visiteds[:]
                del costs_table[:]
                del visiteds[:]
                del pre_global_visiteds[:]
                construct()


def generate_sequence(current_node, garage, local_cost):
    global size_global_visiteds, count_infact

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
                # ####################################
                # # Preve os candidatos do possivel destino
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
                future_limit = future_min_s + (alpha)*(future_max_s - future_min_s)
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


def setOutput(alpha, input_file_name):
    alpha_str = str(alpha).split(".")
    alpha_int = alpha_str[0]
    if len(alpha_str) > 1:
        alpha_dec = alpha_str[1]
    else:
        alpha_dec = "00"
    output_name = "output_files/output_"+input_file_name.split(".")[0]+"_"+alpha_int+"_"+alpha_dec+".txt"
    open(output_name, 'w').close()
    return output_name


def getAlpha():
    alpha = float(raw_input("Alpha (between 0.0 and 1.0): "))
    if alpha < 0.0 or alpha > 1.0:
        print("Out of range. Try again!")
        getAlpha()
    return alpha

def file_writer(output_file, total_cost, solution, vehicles, current_seed, current_time):
    file = open(output_file,"a")
    file.write("\nCost: "+str(total_cost)+" | Vehicles: "+str(vehicles)+" | Seed: "+str(current_seed)+" | Time(s): "+str("{0:.2f}".format(current_time)))
    # file.write("\nSolucao: ")
    # for sequence in solution:
    #     garage = sequence[0]
    #     file.write("\n(K="+str(garage)+") -> ")
    #     first = True
    #     for trip in sequence:
    #         if trip == garage:
    #             if not first:
    #                 file.write("(K="+str(garage)+")")
    #         else:
    #             file.write("(i="+str(trip)+") -> ")
    #         first = False
    # file.write("\n")
    file.close()

def matchTest(pre_x,x,suc_x,pre_y,y,suc_y):
    global current_optimal_cost
    if graph[x][suc_y] != -1 and graph[pre_y][x] != -1:
        if graph[pre_x][y] != -1 and graph[y][suc_x] != -1:
            new_cost_x = graph[x][suc_y] + graph[pre_y][x]
            new_cost_y = graph[pre_x][y] + graph[y][suc_x]
            cost_x = graph[pre_x][x] + graph[x][suc_x]
            cost_y = graph[pre_y][y] + graph[y][suc_y]
            original = cost_x + cost_y
            new = new_cost_x + new_cost_y

            if new < original:
                current_optimal_cost = current_optimal_cost - (original - new)
                return True
    return False

def local(seq,i):
    sequence = seq
    index_x = i
    trip_x = solution[sequence][index_x]
    pre_trip_x = solution[sequence][index_x-1]
    suc_trip_x = solution[sequence][index_x+1]
    controle = 0
    for s in range(len(solution)):
        if s != sequence:
            for t in range(1,len(solution[s])-1): ## Exceto garagens
                index_y = t
                trip_y = solution[s][index_y]
                pre_trip_y = solution[s][index_y-1]
                suc_trip_y = solution[s][index_y+1]
                if matchTest(pre_trip_x, trip_x, suc_trip_x, pre_trip_y, trip_y, suc_trip_y):
                    solution[sequence][index_x] = trip_y
                    solution[s][index_y] = trip_x
                    controle = 1
                    break
        if controle == 1:
            break
    return False
