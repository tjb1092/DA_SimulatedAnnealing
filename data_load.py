import os
import sys
import random

class Node:
    def __init__(self, name, group):
        self.name = name
        self.group = group
        self.nbrs = {}  # constant time lookup for membership/weight

class Graph:
    def __init__(self):
      self.nodes = {}  # constant time lookup for membership/weight

    def add_node(self, name):
        if name <= self.num_cells//2:
            group = 1
        else:
            group = 0
        self.nodes[name] = Node(name, group)
    def add_edge(self, edge):
        #edge is a tuple of length 1, 2
        # add 0th entry to dict if it currently doesn't exist
        if edge[0] not in self.nodes:
            self.add_node(edge[0])
        if len(edge) > 1:
            # add 1st entry to dict if it currently doesn't exist
            if edge[1] not in self.nodes:
                self.add_node(edge[1])
            # add 0->1 edge
            if edge[0] in self.nodes[edge[1]].nbrs:
                # if it's a repeat, add 1 to "weight"
                self.nodes[edge[1]].nbrs[edge[0]] += 1
            else:
                #else, create connection
                self.nodes[edge[1]].nbrs[edge[0]] = 1

            # add 1->0 edge
            if edge[1] in self.nodes[edge[0]].nbrs:
                # if it's a repeat, add 1 to "weight"
                self.nodes[edge[0]].nbrs[edge[1]] += 1
            else:
                #else, create connection
                self.nodes[edge[0]].nbrs[edge[1]] = 1


def data_load(folder, fn):

    with open(os.path.join(folder, fn)) as f:
        content = f.readlines()

    graph = Graph()

    graph.num_cells = int(content[0][:-1])
    graph.num_nets = int(content[1][:-1])

    print(graph.num_cells, graph.num_nets)
    if folder == "examples":
        # skip last row b/c it's a return char
        for row in content[2:-1]:
            nodes = row.split(" ")
            if len(nodes) == 1:
                edge = [int(nodes[0][:-1])]  # remove the newline char
            else:
                edge = [int(nodes[0]), int(nodes[1][:-1])]  # In 1st entry, remove the newline char

            graph.add_edge(edge)
    else:
        for row in content:
            nodes = row.split(" ")

            if len(nodes) == 1:
                edge = [int(nodes[0][:-1])] # remove the newline char
            else:
                edge = [int(nodes[0]), int(nodes[1])]  # In 1st entry, remove the newline char

            graph.add_edge(edge)

    for node in graph.nodes.values():
        print(node.name, [x for x in node.nbrs], [x for x in node.nbrs.values()])

    return graph





def main():
    #folder, fn = "Benchmarks", "b_100_500"

    folder, fn = "examples", "bench_2.net"
    data_load(folder, fn)


if __name__ == "__main__":
    main()
