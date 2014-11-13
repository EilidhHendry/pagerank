__author__ = 'eilidhhendry'

import collections

inputfile = "/Users/eilidhhendry/PycharmProjects/tts4/graph.txt"

incoming = {}
outgoing = {}


def parse(line):
    line = line.strip()
    tokens = line.split()
    id = tokens[0]
    sender = tokens[1]
    recipient = tokens[2]
    return id, sender, recipient


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
    numNodes = len(incoming.keys())
    initialPR = 1.0 / numNodes
    initialDict = {}
    for node in set(incoming.keys()+outgoing.keys()):
        initialDict[node]=initialPR
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


def create_graph(infile):
    for line in infile:
        id, sender, recipient = parse(line)
        if sender in outgoing:
            outgoing[sender].append(recipient)
        else:
            outgoing[sender] = []
            outgoing[sender].append(recipient)
        if recipient not in outgoing:
            outgoing[recipient] = []
        if recipient in incoming:
            incoming[recipient].append(sender)
        else:
            incoming[recipient] = []
            incoming[recipient].append(sender)
        if sender not in incoming:
            incoming[sender] = []


def find_top(ranks):
    output = open('pr.txt', 'w')
    score_rank = {}
    for email, score in ranks.iteritems():
        score_rank[score] = email
    sorted_rank = collections.OrderedDict(sorted(score_rank.items()))
    count = 0
    for score, email in sorted_rank.iteritems():
        if count == 100: break
        print >>output, score, email
        count += 1


def main():
    with open(inputfile) as infile:
        create_graph(infile)
        ranks = page_rank(10)
        print ranks['john.lavorato@enron.com']
        print ranks['jeff.dasovich@enron.com']
        find_top(ranks)


if __name__ == '__main__':
    main()
