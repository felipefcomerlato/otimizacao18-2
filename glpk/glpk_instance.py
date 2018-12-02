def set(table):
    graph = []
    for line in range(len(table)):
        if line > 0:
            graph.append([])
            for cost in table[line]:
                graph[line-1].append(int(cost))
    return graph


def file_writer(graph, k_garages, trips, capacities, file_name):
    file = open("input_"+file_name.split(".")[0]+".dat", 'w')

    file.write("data;\n")
    file.write("set V :=")
    for v in range(1,k_garages+trips+1):
        file.write(" "+str(v))
    file.write(";\n")
    file.write("set K :=")
    for k in range(1,k_garages+1):
        file.write(" "+str(k))
    file.write(";\n")
    file.write("set T :=")
    for t in range(k_garages+1,k_garages+trips+1):
        file.write(" "+str(t))
    file.write(";\n\n")

    file.write("param C :=")
    for c in range(1,k_garages+1):
        file.write("\n"+str(c)+" "+str(capacities[c-1]))
    file.write(" ;\n\n")

    file.write("param COST:\n   ")
    for j in range(1,k_garages+trips+1):
        file.write(str(j)+" ")
    file.write(":=")

    for i in range(1,k_garages+trips+1):
        file.write("\n"+str(i)+" ")
        for cost in graph[i-1]:
            file.write(str(cost)+" ")
    file.write(";\n\n")
    file.write("end;")













    file.close()
