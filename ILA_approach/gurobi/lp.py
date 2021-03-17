#!/usr/bin/env python3.7

# Copyright 2020, Gurobi Optimization, LLC

# This example reads an LP model from a file and solves it.
# If the model is infeasible or unbounded, the example turns off
# presolve and solves the model again. If the model is infeasible,
# the example computes an Irreducible Inconsistent Subsystem (IIS),
# and writes it to a file

import collections
ROWS = 6
COLS = 12

def get_neighbors_for_node(node_name):
    # default case
    node_row = int(node_name[find_nth(node_name, "_", 1)+1:find_nth(node_name, "_", 2)])
    node_col = int(node_name[find_nth(node_name, "_", 2)+1:])
    top_row = (node_row - 1) if (node_row != 0) else ROWS-1
    top_col = node_col
    bot_row = (node_row + 1) if (node_row != ROWS-1) else 0
    bot_col = node_col
    left_row = node_row
    left_col = (node_col - 1) if (node_col != 0) else COLS-1
    right_row = node_row
    right_col = (node_col + 1) if (node_col != COLS-1) else 0
    # return [[top_row, top_col], [right_row, right_col], [bot_row, bot_col], [left_row, left_col]]
    return ["N_" + str(top_row) + "_" + str(top_col), "N_" + str(right_row) + "_" + str(right_col), "N_" + str(bot_row) + "_" + str(bot_col), "N_" + str(left_row) + "_" + str(left_col)]

# helper routines
def create_routing_table_from_array_of_lp_variables(packets_in_nodes):
    # create a dict where eac packet would be an item
    routes = {}
    for x in packets_in_nodes:
        packet_name = x[:find_nth(x, '_', 3)] # cuts out the packet name
        if (packet_name in routes.keys()):
            routes[packet_name].append(x)
            routes[packet_name].sort()
        else:
            routes[packet_name] = [x];
    # print(routes)
    f = open("routes.txt", "w")
    for key, value in routes.items():
        f.write(str(key)+ ' : '+ str(value))
        f.write("\n\n")
    f.write("\n\n")
    f.write("\n\n")
    f.write("\n\n")
    f.write("\n\n")
    f.write("======== LOAD BALANCE =============\n")
    south = 0
    north = 0
    west = 0
    east = 0
    for x in packets_in_nodes:
        if(x[-5:]== "N_0_1"):
            east = east + 1
        elif (x[-5:] == "N_1_0"):
            south = south + 1
        elif (x[-6:] == "N_0_11"):
            west = west + 1
        elif (x[-5:]=="N_5_0"):
            north = north + 1
    f.write("NORTH - " + str(north) + "\n")
    f.write("SOUTH - " + str(south) + "\n")
    f.write("WEST - " + str(west) + "\n")
    f.write("EAST - " + str(east) + "\n")
    f.write(str(len(routes)))

    f.write("\n\n")
    f.write("\n\n")
    f.write("\n\n")
    f.write("======== CONFLICTS =============\n")
    packets_at_cycles = {}
    for x in packets_in_nodes:
        packet_cycle = int(x[find_nth(x, '_', 4)+1:find_nth(x, '_', 5)])
        current_node = x[find_nth(x, '_', 5)+1:]
        if (packet_cycle in packets_at_cycles.keys()):
            if(current_node in packets_at_cycles[packet_cycle].keys()):
                packets_at_cycles[packet_cycle][current_node].append(x)
                packets_at_cycles[packet_cycle][current_node].sort()
            else:
                packets_at_cycles[packet_cycle][current_node] = [x]
        else:    
            packets_at_cycles[packet_cycle] = {}
            packets_at_cycles[packet_cycle][current_node] = [x] 

    packets_at_cycles = collections.OrderedDict(sorted(packets_at_cycles.items()))
    for key, value in packets_at_cycles.items():
        f.write(str(key)+ ' : '+ str(value))
        f.write("\n\n")
    # print(packets_at_cycles)
    #

    for cycle, nodes_having_packets in packets_at_cycles.items():
        if(cycle == packets_at_cycles.keys()[-1]):
            continue
        for node, packets_at_node in nodes_having_packets.items(): 
            if(len(packets_at_node)>=2): # if there are 2 and more nodes in one packet at one cycle, its possible that the same nodes are in same other node on the next cycle
                list1_as_set = set(packets_at_node)
                neighbors_of_node = get_neighbors_for_node(node)
                # print neighbors_of_node
                #
                # MISTAKE SOMEWHERE HERE
                #
                #
                if(neighbors_of_node[0] in packets_at_cycles[cycle+1].items()):
                    if(len(list1_as_set.intersection(packets_at_cycles[cycle+1][neighbors_of_node[0]])) >=1):
                        print "\n\n\nFOUND CONFLICTS\n\n\n"
                if(neighbors_of_node[1] in packets_at_cycles[cycle+1].items()):
                    if(len(list1_as_set.intersection(packets_at_cycles[cycle+1][neighbors_of_node[1]])) >=1):
                        print "\n\n\nFOUND CONFLICTS\n\n\n"
                if(neighbors_of_node[2] in packets_at_cycles[cycle+1].items()):
                    if(len(list1_as_set.intersection(packets_at_cycles[cycle+1][neighbors_of_node[2]])) >=1):
                        print "\n\n\nFOUND CONFLICTS\n\n\n"
                if(neighbors_of_node[3] in packets_at_cycles[cycle+1].items()):
                    if(len(list1_as_set.intersection(packets_at_cycles[cycle+1][neighbors_of_node[3]])) >=1):
                        print "\n\n\nFOUND CONFLICTS\n\n\n"
                # print ("found a conflict - " + ) str(len(list1_as_set.intersection(packets_at_cycles[cycle+1])))

    for i in range(len(packets_in_nodes)-1):
        for j in range(i+1, len(packets_in_nodes)):
            if(packets_in_nodes[i][find_nth(x, '_', 2):] == packets_in_nodes[j][find_nth(x, '_', 2):] and packets_in_nodes[i][find_nth(packets_in_nodes[i], '_', 5):]!="_N_0_0"):
                print("duplicate found for " + packets_in_nodes[i] + " and " + packets_in_nodes[j] + "\n")






    f.close()

def find_nth(string, substring, what_occurance):
    start = string.find(substring)
    while start >= 0 and what_occurance > 1:
        start = string.find(substring, start+len(substring))
        what_occurance -= 1
    return start




import sys
import gurobipy as gp
from gurobipy import GRB

if len(sys.argv) < 2:
    print('Usage: lp.py filename')
    sys.exit(0)

# Read and solve model

model = gp.read(sys.argv[1])
model.optimize()

if model.status == GRB.INF_OR_UNBD:
    # Turn presolve off to determine whether model is infeasible
    # or unbounded
    model.setParam(GRB.Param.Presolve, 0)
    model.optimize()

if model.status == GRB.OPTIMAL:
    print('Optimal objective: %g' % model.objVal)
    model.write('model.sol')
    variables_solved = model.getVars()
    packets_in_nodes = [var.VarName for var in variables_solved if var.x==1.0]
    # print(packets_in_nodes)
    create_routing_table_from_array_of_lp_variables(packets_in_nodes)
    sys.exit(0)

elif model.status != GRB.INFEASIBLE:
    print('Optimization was stopped with status %d' % model.status)
    sys.exit(0)


# Model is infeasible - compute an Irreducible Inconsistent Subsystem (IIS)

print('')
print('Model is infeasible')
model.computeIIS()
model.write("model.ilp")
print("IIS written to file 'model.ilp'")





