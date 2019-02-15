from data_load  import data_load, GroupLst
import math
import random
import copy
import time
import os

def acceptMove(delCost, T, num_cells):
    if delCost < 0:
        return True
    else:
        boltz = math.exp((-(delCost*num_cells))/(T))
        r = random.uniform(0, 1)
        if r < boltz:
            return True
        else:
            return False

def coolDown(T, params):
    return T * params["Trate"]

def heatUp(T, params):
    T = params["Theat"]
    params["Theat"] = params["factor"] * params["Theat"]
    return T, params

def simulatedAnnealing(graph, num_cells, params):
    curSol, nextSol = GroupLst(graph, num_cells), GroupLst(graph, num_cells)
    bestSol = copy.deepcopy(curSol)
    T = params["T0"]
    last_time, total_time = time.time(), time.time()
    cntr, tol_cntr = 0, 0
    while T > params["Tfreeze"]:
        for i in range(params["num_moves_per_T"]):

            nextSol.V, nextSol.cost = list(curSol.V), curSol.cost
            nextSol.perturb()
            delCost = nextSol.cost - curSol.cost

            if acceptMove(delCost, T, num_cells):
                curSol.V, curSol.cost = list(nextSol.V), nextSol.cost
                tol_cntr = 0
            else:
                tol_cntr += 1
            if curSol.cost < bestSol.cost:
                bestSol.V, bestSol.cost = list(curSol.V), curSol.cost

        cntr += 1
        print("{} T: {} curCost: {}".format(cntr, T, curSol.cost))
        print('T took {:0.3f} seconds'.format(time.time()-last_time))

        last_time = time.time()
        if tol_cntr < params["tolerance"] or params["Theat"] < params["Tfreeze"]:
            T = coolDown(T, params)
        elif params["Theat"] > params["Tfreeze"]:
            # condition prevents heatup if it actually cools system down.
            T, params = heatUp(T, params)
            tol_cntr = 0


    print("Best Cost: {}, temp iteration {}".format(bestSol.cost, cntr))
    print("Total Time {:0.3f} seconds".format(time.time()-total_time))
    return bestSol

def writeResults(solution, fn):
    f = open(os.path.join("Results", "R_" + fn), "w")
    newline = str(solution.cost)+ "\n"
    f.write(newline)
    A, B = "", ""
    for i, n in enumerate(solution.V):
        if n == 0:
            A += (str(i+1) + " ")
        else:
            B += (str(i+1) + " ")

    f.write(A+"\n")
    f.write(B+"\n")
    f.close()




def main():
    folder, header, fn = "Benchmarks", "b_", "250000_1000000"
    #folder, header, fn = "examples", "bench_", "16.net"
    graph, num_cells, num_nets = data_load(folder, header + fn)

    nmpt = int(0.02*num_nets+10)
    print("num moves per T {}".format(nmpt))

    params = {"T0": 10000, "Tfreeze": 0.01, "num_moves_per_T": nmpt,
              "Trate":0.99, "Theat": 5000, "factor": 0.5, "tolerance": nmpt*100}  # k=1, so it won't be considered


    solution = simulatedAnnealing(graph, num_cells, params)
    writeResults(solution, fn)
    print("num moves per T {}".format(nmpt))


if __name__ == "__main__":
    main()
