__author__ = 'eilidhhendry'

import creategraph
import math

incoming = {}
outgoing = {}

filename = "/Users/eilidhhendry/PycharmProjects/tts4/graph.txt"


def hits(numIterations):
    global incoming
    global outgoing
    current_hub = {}
    current_auth = {}
    for iteration in xrange(1,numIterations):
        print 'running iteration ', iteration
        if iteration == 1:
            current_hub = initialise_hits()
            current_auth = initialise_hits()
            print 'hub: ', current_hub['jeff.dasovich@enron.com']
            print 'auth: ', current_auth['jeff.dasovich@enron.com']
        current_hub, current_auth = update_hub(current_hub, current_auth)
        current_hub = normalise(current_hub)
        current_auth = normalise(current_auth)
    return current_hub, current_auth


def initialise_hits():
    global incoming
    global outgoing
    print 'initialising scores'
    numNodes = len(incoming.keys())
    initial_score = 1.0 / math.sqrt(numNodes)
    initialise_dict = {}
    for node in incoming.keys():
        initialise_dict[node] = initial_score
    return initialise_dict


# hub has lots of outgoing
# auth has lots of incoming
def update_hub(current_hub, current_auth):
    new_hub = {}
    for node in current_hub.keys():
        score = 0
        for email in outgoing[node]:
            score += current_auth[email]
        new_hub[node] = score
    new_auth = {}
    for node in current_auth.keys():
        score = 0
        for email in incoming[node]:
            score += current_hub[email]
        new_auth[node] = score
    return new_hub, new_auth


def normalise(current_dict):
    new_dict = {}
    total_score = math.sqrt(sum(score*score for score in current_dict.values()))
    for key, value in current_dict.items():
        new_dict[key] = value / total_score
    return new_dict


def main():
    global incoming
    global outgoing
    with open(filename) as infile:
        incoming, outgoing = creategraph.create_graph(infile)
        hubs, auths = hits(10)
        print 'hub: ', hubs['jeff.dasovich@enron.com']
        print 'auth: ', auths['jeff.dasovich@enron.com']

if __name__=='__main__':
    main()
