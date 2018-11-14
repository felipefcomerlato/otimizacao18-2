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
# grafo = [
#             [(4,1), (3,2), (2,4), (1,10)],
#             [(4,7), (3,6), (2,12), (0,10)],
#             [(1,12), (3,3), (0,4), (4,6)],
#             [(4,5), (0,2), (1,6), (2,3)],
#             [(0,1), (1,7), (2,6), (3,5)]
#         ]

# grafo = [
#             [-1, -1, 5032, 5028, 5025, 5073],
#             [-1, -1, 5070, 5067, 5026, 5047],
#             [5023, 5019, -1, -1, 138, 248],
#             [5052, 5059, -1, -1, 332, 212],
#             [5061, 5062, -1, -1, -1, 84],
#             [5053, 5023, -1, -1, -1, -1]
#         ]

grafo = [
            [-1, -1, 5032, 5028, 5025, 5073],
            [-1, -1, 5070, 5067, 5026, 5047],
            [5023, -1, -1, -1, 138, 248],
            [5052, -1, -1, -1, 332, 212],
            [5061, -1, -1, -1, -1, 84],
            [5053, -1, -1, -1, -1, -1]
        ]

# for nodo in range(len(grafo)):
#     for arco in range(len(grafo[nodo])):
#         if nodo == 1:
#             print(grafo[nodo][arco][1]) # Printa todos local_costs de arcos ligados ao nodo 1
alpha = 0.2
init_node = 0
current_node = init_node
candidatos = []
rcl = []
solution = []
solution.append(init_node)
cost = 0
visiteds = []

print("\nNodo inicial: " + str(init_node) + "\n")

def construct(current_node, cost):

    print("Nodo atual: " + str(current_node))

    ## Gera os candidatos a partir do nodo atual
    for dest in range(len(grafo[current_node])):
        if dest == 0: ## Nao add candidato quando o destino eh o nodo inicial (garagem)
            finally_dest = dest ## Salva para uso final
        elif dest not in visiteds:
            if grafo[current_node][dest] != -1:
                candidatos.append(dest)


#########################################################################
#####-----OS NODOS VISITADOS SAO CUMULATIVOS ATE PASSAR POR TODAS GARAGENS
#########################################################################
    ## Atualiza lista de nodos ja visitados
    visiteds.append(current_node)

    ## Se nao ha candidatos, adiciona na solucao o caminho de volta a origem
    if len(candidatos) == 0:
        solution.append(finally_dest)
        cost = cost + grafo[current_node][finally_dest]
        print("Unico destino possivel: garagem\n")
        print("Nodo final: " + str(finally_dest) + "\n")
        print("Solucao final: "+str(solution))
        print("Custo: "+str(cost))
        return 0

    ## Extrai local_costs dos candidatos
    local_costs = []
    for c in candidatos:
        local_costs.append((c, grafo[current_node][c]))

    ## Pega o maior e menor custo entre os Candidatos
    ## e calcula o limitante com base no fator alpha
    max_s = max(local_costs,key=lambda item:item[1])[1]
    min_s = min(local_costs,key=lambda item:item[1])[1]
    limit = min_s + alpha*(max_s - min_s)

    ## Gera o RCL com base nos candidatos de custo abaixo do limitante
    for c in candidatos:
        if grafo[current_node][c] <= limit:
            rcl.append(c)

    ## Escolhe um caminho a seguir aleatoriamente dentre o contidos em RCL
    choice = random.randrange(0,len(rcl))
    solution.append(rcl[choice])
    cost = cost + grafo[current_node][rcl[choice]]
    # copia = copy.deepcopy(origem)

    print("Candidatos: " + str(candidatos))
    print("Max: " + str(max_s) + " / Min: " + str(min_s) + " / Limit: " + str(limit))
    print("RCL: " + str(rcl) + " / Dest escolhido: " + str(rcl[choice]))
    print("\n--------\n")
    current_node = rcl[choice]
    del candidatos[:]
    del rcl[:]
    construct(current_node, cost)

# print(max(candidatos,key=itemgetter(1))[0])
construct(current_node, cost)
#...
