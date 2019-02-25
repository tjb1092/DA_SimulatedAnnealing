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
      # initialize group array to have 50% group A and 50% group B.
      self.V = [0]*(self.num_cells//2) + [1]*(self.num_cells//2)
      random.shuffle(self.V)  # initialize random partition
      self.init_cost()  # Initialize the cost of the random partition

    def init_cost(self):
        cost = 0
        for i, n in enumerate(self.V):
            # Find 0 nodes w/ connections in 1
            if n == 0:
                if i+1 in self.graph.nodes:
                    for nbr in self.graph.nodes[i+1].nbrs:
                        if self.V[nbr-1] == 1:
                            # Add their weights
                            cost += self.graph.nodes[i+1].nbrs[nbr]
        self.cost = cost

    def perturb(self):
        # randomly switch two cells
        A = random.randint(0,self.num_cells-1)
        chosen = False
        while not chosen:
            # Ensures that the B cell is not in A
            B = random.randint(0,self.num_cells-1)
            if B == A or self.V[B] == self.V[A]:
                continue
            else:
                chosen = True
        # Switch the groups
        self.V[A], self.V[B] = int(not(self.V[A])), int(not(self.V[B]))

        # Update the costs based on that move
        self.update_cost(A+1, B+1)  # The +1 offsets the 0-index of the list
        self.update_cost(B+1, A+1)

    def update_cost(self, A, B):
        # get A's group
        gA = self.V[A-1]
        if A in self.graph.nodes:
            # Traverse through all of A's nbrs.
            for nbr in self.graph.nodes[A].nbrs:
                if self.V[nbr-1] == gA and nbr != (B):
                    # Reduce cost if nbr is now in the same group as A
                    self.cost = self.cost - self.graph.nodes[A].nbrs[nbr]
                elif self.V[nbr-1] != gA and nbr != (B):
                    # Increase "    "
                    self.cost = self.cost + self.graph.nodes[A].nbrs[nbr]

def data_load(fn):

    with open(fn) as f:
        content = f.readlines()
        f.close()

    num_cells, num_nets = int(content[0][:-1]), int(content[1][:-1])
    graph = Graph()

    print(num_cells, num_nets)
    if fn[1] == "e":
        #i.e. it's a "bench" file.

        # skip last row b/c it's a return char
        for row in content[2:-1]:
            nodes = row.split(" ")
            if len(nodes) == 1:
                edge = [int(nodes[0][:-1])]  # remove the newline char
            else:
                edge = [int(nodes[0]), int(nodes[1][:-1])]  # In 1st entry, remove the newline char

            graph.add_edge(edge)
    else:
        # File is a "b_"
        for row in content:
            nodes = row.split(" ")

            if len(nodes) == 1:
                edge = [int(nodes[0][:-1])] # remove the newline char
            else:
                edge = [int(nodes[0]), int(nodes[1])]  # In 1st entry, remove the newline char

            graph.add_edge(edge)

    return graph, num_cells, num_nets


def writeResults(solution, cost, fn):
    # Write the cost and cutsets to an output file.
    f = open("Results/{}".format(fn), "w")
    newline = str(cost)+ "\n"  # Generate cost string
    f.write(newline)
    A, B = "", ""
    # Generate strings for the A group and the B group
    for i, n in enumerate(solution):
        if n == 0:
            A += (str(i+1) + " ")
        else:
            B += (str(i+1) + " ")

    f.write(A+"\n")
    f.write(B+"\n")
    f.close()
