__author__ = 'eilidhhendry'

import creategraph

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
        incoming, outgoing = create_id_graph(graphfile, key_people)
    print 'created graphs'

    # find the subject lines of the key people
    subjects = {}
    with open(subjectfile) as infile:
        for line in infile:
            msgid, subject = read_subjects(line)
            if msgid in incoming.values() or msgid in outgoing.values():
                subjects[msgid] = subject

    print incoming.items()
    print outgoing.items()
    print subjects.items()

if __name__ == '__main__':
    main()

