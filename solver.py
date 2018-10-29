#!/usr/bin/python3

import random
import json
from person import person
from links import link, linklist, chain
        
p = []
#links = linklist()

with open("sample.json", 'r') as f:
    data = (json.load(f))
    #print(data)
    
for family in data["people"]["families"]:
    famname = family["name"]
    for memberkey in family["members"].keys():
        membername = memberkey
        memberemail = family["members"][memberkey]["email"]
        #print("{}: {}".format(famname, membername))
        p.append(person("{}_{}".format(famname, membername), membername, famname))

    
#sys.exit()
def generateLinks():
    links = linklist()
    for pers in p:
        #print(pers.code)
        #print(pers.name)
        for otherpers in p:
            if pers.family != otherpers.family:
                links.append(link(pers, otherpers))
    return links

# init people
# build links
# remove links

# traverse links


# is link valid?
# link is invalid if it links two family members, or someone to themselves
def isValidLink(l):
    if l.source.family == l.destination.family or l.source.code == l.destination.code:
        return False
    else:
        return True
        
# is chain valid? check all links
# and potentially check all other chains
def isValidChain(c):
    for l in c:
        if not isValidLink(l):
            return False
    return True
    
def generateChain(depth=0):
    if depth > 5:
        print("Error: Depth maximum reached.")
        return chain()
    # store gift giving chain
    combo = chain()
    # create links
    links = generateLinks()

    # grab first person, since chain is a loop it wont matter
    curpers = p[0]
    # select from their out-links
    while len(links) > 0:
        randlinknum = random.randint(0, len(links.fromsrc(curpers.code)) - 1)

        sellink = links.fromsrc(curpers.code)[randlinknum]

        # nobody should be able to get FROM curpers
        links.rem_lis(links.fromsrc(curpers.code))
        
        # nobody should be able to give TO the destination person
        links.rem_lis(links.todest(sellink.destination.code))
        links.rem_lis(links.todest(curpers.code))

        # set curpers to the new person
        curpers = sellink.destination
        combo.append(sellink)

        
    combo.append(link(combo[len(combo) - 1].destination, combo[0].source))
    
    if isValidChain(combo):
        return combo
    else:
        return generateChain(depth + 1)
        
# can still generate invalid if two family members are picked first and last
# since it just ties them together
# therefore we need to do a validity check and prepare to calculate again

gift_chain = generateChain()

print(gift_chain)
