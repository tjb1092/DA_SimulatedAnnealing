from data_handler  import data_load, GroupLst, Graph
from pympler import classtracker
import argparse

def main():
    cltr = classtracker.ClassTracker()
    cltr.track_class(GroupLst)
    cltr.create_snapshot()
    # Needed for the specified command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, default="bench_2.net",
                        help='What is the input filename?')
    args = parser.parse_args()

    # Load the input data and generate the graph
    graph, num_cells, num_nets = data_load(args.i)
    # Instantiate GroupLst
    Sol, nSol = GroupLst(graph, num_cells), GroupLst(graph, num_cells)
    print("Graph Created")
    # Report the memory size
    cltr.create_snapshot()
    cltr.stats.print_summary()


if __name__ == "__main__":
    main()
