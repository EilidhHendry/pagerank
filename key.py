__author__ = 'eilidhhendry'

import creategraph
import pydot

subjectfile = '/Users/eilidhhendry/PycharmProjects/tts4/subject.txt'
graph = '/Users/eilidhhendry/PycharmProjects/tts4/graph.txt'
auth = '/Users/eilidhhendry/PycharmProjects/tts4/auth.txt'
hubs = '/Users/eilidhhendry/PycharmProjects/tts4/hubs.txt'


def get_top(infile):
    count = 0
    top = []
    for line in infile:
        if count == 5: break
        tokens = line.split()
        top.append(tokens[1])
        count += 1
    return top


def read_subjects(line):
    line = line.strip()
    tokens = line.split()
    msgid = tokens[0]
    subject = tokens[1:]
    return msgid, subject


def create_id_graph(infile, key_people):
    incoming = {}
    outgoing = {}
    for line in infile:
        msgid, sender, recipient = creategraph.parse(line)
        if sender != recipient:
            if (sender in key_people) or (recipient in key_people):
                if sender in outgoing:
                    outgoing[sender].append((recipient, msgid))
                else:
                    outgoing[sender] = []
                    outgoing[sender].append((recipient, msgid))
                if recipient not in outgoing:
                    outgoing[recipient] = []
                if recipient in incoming:
                    incoming[recipient].append((sender, msgid))
                else:
                    incoming[recipient] = []
                    incoming[recipient].append((sender, msgid))
                if sender not in incoming:
                    incoming[sender] = []
    assert incoming.keys() == outgoing.keys()
    return incoming, outgoing

def create_graph(infile):
    incoming = {}
    outgoing = {}
    for line in infile:
        msgid, sender, recipient = creategraph.parse(line)
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

def create_graph(incoming, outgoing):
    graph = pydot.Dot(graph_type='digraph')
    for email in incoming.keys():
        node = pydot.Node(email)
        graph.add_node(node)
    for email, list in incoming.items():
        node_a = pydot.Node(email)
        for sender in list:
            node_b = pydot.Node(sender)
            graph.add_edge(pydot.Edge(node_b, node_a))
    for email, list in outgoing.items():
        node_a = pydot.Node(email)
        for recipient in list:
            node_b = pydot.Node(recipient)
            graph.add_edge(pydot.Edge(node_a, node_b))
    graph.write_png('example.png')

def main():
    # get the top 5 from the auth file
    with open(auth) as authfile:
        top_auth = get_top(authfile)

    # get the top 5 from the hubs file
    with open(hubs) as hubsfile:
        top_hubs = get_top(hubsfile)

    # create a list of key people
    key_people = top_auth + top_hubs
    print key_people

    # create the graph including msg ids of key people
    with open(graph) as graphfile:
        incoming, outgoing = create_graph(graphfile)
    print 'created graphs'

    create_graph(incoming, outgoing)
    #values = [x for x in (incoming.values()+outgoing.values()) if x]
    #ids = []
    #for list in values:
    #    for email, msgid in list:
    #        ids.append(msgid)
    #print ids[0:5]


    # find the subject lines of the key people
    #subjects = {}
    #with open(subjectfile) as infile:
    #    for line in infile:
    #        msgid, subject = read_subjects(line)
    #        if msgid in ids:
    #            subjects[msgid] = subject

    #print incoming.items()[0:5]
    #print outgoing.items()[0:5]
    #print subjects.items()[0:5]

if __name__ == '__main__':
    main()

