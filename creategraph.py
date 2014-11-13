__author__ = 'eilidhhendry'

import collections

def create_graph(infile):
    incoming = {}
    outgoing = {}
    for line in infile:
        id, sender, recipient = parse(line)
        if sender != recipient:
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
    assert incoming.keys() == outgoing.keys()
    return incoming, outgoing


def parse(line):
    line = line.strip()
    tokens = line.split()
    if len(tokens) > 3:
        print tokens
    id = tokens[0]
    sender = tokens[1]
    recipient = tokens[2]
    return id, sender, recipient


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
