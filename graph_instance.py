def set(table):
    graph = []
    for line in range(len(table)):
        if line > 0:
            graph.append([])
            for cost in table[line]:
                graph[line-1].append(int(cost))
    return graph
