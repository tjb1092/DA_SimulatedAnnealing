import os
import random

class Node:
    def __init__(self, name):
        self.name = name
        self.nbrs = {}  # constant time lookup for membership/weight

class Graph:
    def __init__(self):
      self.nodes = {}  # constant time lookup for membership/weight

    def add_edge(self, edge):
        #edge is a tuple of length 1, 2
        # add 0th entry to dict if it currently doesn't exist
        if edge[0] not in self.nodes:
            self.nodes[edge[0]] = Node(edge[0])
        if len(edge) > 1:
            # add 1st entry to dict if it currently doesn't exist
            if edge[1] not in self.nodes:
                self.nodes[edge[1]] = Node(edge[1])
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

class GroupLst:
    def __init__(self, graph, num_cells):
      self.graph = graph  # pointer to adjacency list
      self.num_cells = num_cells
      V0 = [0]*(self.num_cells//2)
      V1 = [1]*(self.num_cells//2)
      self.V = V0 + V1
      random.shuffle(self.V)
      self.init_cost()

    def perturb(self):
        # randomly switch two cells
        A = random.randint(0,self.num_cells-1)
        chosen = False
        while not chosen:
            B = random.randint(0,self.num_cells-1)
            if B == A or self.V[B] == self.V[A]:
                continue
            else:
                chosen = True
        self.V[A], self.V[B] = int(not(self.V[A])), int(not(self.V[B]))

        self.update_cost(A+1, B+1)
        self.update_cost(B+1, A+1)

    def init_cost(self):
        cost = 0
        for i, n in enumerate(self.V):
            # Find 0 nodes w/ connections in 1
            if n == 0:
                if i+1 in self.graph.nodes:
                    for nbr in self.graph.nodes[i+1].nbrs:
                        if self.V[nbr-1] == 1:
                            cost += self.graph.nodes[i+1].nbrs[nbr]
        self.cost = cost

    def update_cost(self, A, B):
        gA= self.V[A-1]
        if A in self.graph.nodes:
            for nbr in self.graph.nodes[A].nbrs:
                if self.V[nbr-1] == gA and nbr != (B):
                    self.cost = self.cost - self.graph.nodes[A].nbrs[nbr]
                elif self.V[nbr-1] != gA and nbr != (B):
                    self.cost = self.cost + self.graph.nodes[A].nbrs[nbr]


def data_load(folder, fn):

    with open(os.path.join(folder, fn)) as f:
        content = f.readlines()
        f.close()
        
    num_cells, num_nets = int(content[0][:-1]), int(content[1][:-1])
    graph = Graph()

    print(num_cells, num_nets)
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

    return graph, num_cells, num_nets
