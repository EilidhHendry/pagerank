__author__ = 'eilidhhendry'


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


def read_subjects(infile):
    subjects = {}
    for line in infile:
        line = line.strip()
        tokens = line.split()
        msgid = tokens[0]
        subject = tokens[1:]
        subjects[msgid] = subject
    return subjects


def create_id_graph(infile):
    incoming = {}
    outgoing = {}
    for line in infile:
        msgid, sender, recipient = parse(line)
        if sender != recipient:
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


def parse(line):
    line = line.strip()
    tokens = line.split()
    id = tokens[0]
    sender = tokens[1]
    recipient = tokens[2]
    return id, sender, recipient


def find_top(ranks, filename):
    output = open(filename, 'w')
    score_rank = {}
    for email, score in ranks.iteritems():
        score_rank[score] = email
    #sorted_rank = collections.OrderedDict(sorted(score_rank.iteritems(), key=lambda (x,y):float(x)))
    sorted_rank = sorted(score_rank.iteritems(), key=lambda x: x[0])
    sorted_rank.reverse()
    count = 0
    for score, email in sorted_rank:
        if count == 100: break
        print >>output, score, email
        count += 1
