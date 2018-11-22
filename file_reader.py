


########################################################
# Instructions:
# 1 - Insert instance file in input_files directory
# 2 - Run file_reader
# 3 - Enter file name containing the extension
########################################################


import os
import graph_instance
import grasp

#-------------------------------------------------------

def input_path():
    file_name = raw_input("Enter name of instance file: ")
    load("input_files/"+file_name)

def load(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file_object:
            try:
                getInfos(file_object)
                return True
            except:
                print("Fail while opening file. Try again!\n")
                input_path()
    else:
        print("Name file not exist. Try again!\n")
        input_path()

def getInfos(f):
    content = [x.strip() for x in f.readlines()] # Read lines ignoring '\n'
    first_line = content[:1]
    first_line = first_line[0].split()

    # Get garages, trips and garages capacities from file first line
    garages = int(first_line[0])
    capacities = []
    for g in range(garages):
        capacities.append(first_line[2+g])
    trips = int(first_line[1])

    # Print infos
    print("Garages: "+str(garages))
    print("Trips: "+str(trips))
    for g in range(len(capacities)):
        print("Garagem "+str(g)+" : capacidade "+str(capacities[g]))

    table_lines = []
    for line in content:
        table_lines.append(line.split())

    graph_setted = graph_instance.set(table_lines)
    grasp.run(graph_setted)

# -----------------

input_path()
