__author__ = 'eilidhhendry'

import creategraph

inputfile = "/Users/eilidhhendry/PycharmProjects/tts4/graph.txt"

incoming = {}
outgoing = {}


def page_rank(noIterations):
    global incoming
    global outgoing
    currentPRs = {}
    for iteration in xrange(1, noIterations):
        print 'running iteration ', iteration
        if iteration == 1:
            currentPRs = initialise_pr()
            print 'graph initialised'
        print currentPRs['jeff.dasovich@enron.com']
        print currentPRs['john.lavorato@enron.com']
        currentPRs = update_scores(currentPRs)
    return currentPRs


def initialise_pr():
    global incoming
    global outgoing
    numNodes = len(incoming.keys())
    initialPR = 1.0 / numNodes
    initialDict = {}
    for node in incoming.keys():
        initialDict[node] = initialPR
    return initialDict


def update_scores(currentDict):
    global incoming
    global outgoing
    numNodes = len(incoming.keys())
    lambdaVal = 0.8
    sinkScore = 0
    sinks = sink_nodes()
    for sinkNode in sinks:
        sinkScore += currentDict[sinkNode]
    print sinkScore
    print 'sink nodes calculated'
    newDict = {}
    for node in currentDict.keys():
        incomingN = incoming[node]
        prOther = sum((currentDict[inNode] / len(outgoing[inNode])) for inNode in incomingN)
        prCurrent = ((1-lambdaVal + (lambdaVal * sinkScore)) / numNodes) + (lambdaVal * prOther)
        newDict[node] = prCurrent
    return newDict


def sink_nodes():
    sinks = [node for node in outgoing.keys() if outgoing[node] == []]
    return sinks


def main():
    global incoming
    global outgoing
    with open(inputfile) as infile:
        incoming, outgoing = creategraph.create_graph(infile)
        ranks = page_rank(13)
        print ranks['john.lavorato@enron.com']
        print ranks['jeff.dasovich@enron.com']
        creategraph.find_top(ranks, 'pr.txt')


if __name__ == '__main__':
    main()
