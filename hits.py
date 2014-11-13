__author__ = 'eilidhhendry'

import creategraph

filename = "/Users/eilidhhendry/PycharmProjects/tts4/graph.txt"

def main():
    with open(filename) as infile:
        creategraph.create_graph(infile)

if __name__=='__main__':
    main()
