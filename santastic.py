#!/usr/bin/python3

import random
import json
import argparse
import pickle

from person import person
from links import link, linklist, chain
     
class santastic():     

    people = []

    
    def __init__(self):
        pass
        
    def load_config(self, config_filename="sample.json"):
        try:
            with open(config_filename, 'r') as f:
                data = (json.load(f))
        except:
            print("Error opening file {}".format(config_filename))
            return
            
        try:
            for family in data["people"]["families"]:
                famname = family["name"]
                for memberkey in family["members"].keys():
                    membername = memberkey
                    memberemail = family["members"][memberkey]["email"]
                    memberfullname = family["members"][memberkey]["full name"]

                    self.people.append(person("{}_{}".format(famname, membername), membername, famname, memberemail, memberfullname))

        except TypeError:
            print("Error reading data from file {}".format(config_filename))

    def generateLinks(self):
        links = linklist()
        for pers in self.people:
            for otherpers in self.people:
                if pers.family != otherpers.family:
                    links.append(link(pers, otherpers))
        return links

        # init people
        # build links
        # remove links

        # traverse links

        # is link valid?
        # link is invalid if it links two family members, or someone to themselves
    def isValidLink(self, l):
        if l.source.family == l.destination.family or l.source.code == l.destination.code:
            return False
        else:
            return True
                
    # is chain valid? check all links
    # and potentially check all other chains
    def isValidChain(self, c):
        for l in c:
            if not self.isValidLink(l):
                return False
        return True
        
    def generateChain(self, depth=0):
        if depth > 5:
            print("Error: Depth maximum reached.")
            return chain()
        # store gift giving chain
        combo = chain()
        # create links
        links = self.generateLinks()

        # grab first person, since chain is a loop it wont matter
        print(self.people)
        curpers = self.people[0]
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
        
        if self.isValidChain(combo):
            return combo
        else:
            return self.generateChain(depth + 1)
                
        # can still generate invalid if two family members are picked first and last
        # since it just ties them together
        # therefore we need to do a validity check and prepare to calculate again

    def save_chain(self, chain, filename="secret.santa"):
        try:
            pickle.dump(chain, open(filename, "wb"))
            print("Chain saved as {}".format(filename))
        except:
            print("Chain unable to be saved as {}".format(filename))
        
    def load_chain(self, filename):
        try:
            return pickle.load(open(filename, "rb"))
        except:
            return None

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, help="config file")
    parser.add_argument("-l", "--load", type=str, help="load saved chain filename")
    parser.add_argument("-o", "--save", type=str, help="save chain filename (default: secret.santa)", default="secret.santa")

    args = parser.parse_args()
    
    print(args.config)

    
    santa = santastic()
    if args.config != None:
        santa.load_config(args.config)
    else:
        santa.load_config()

    if args.load != None:
        ch = santa.load_chain(args.load)
    else:
        print("generating chain...")
        ch = santa.generateChain()

    print(ch)
    
    if args.load == None:
        santa.save_chain(ch, args.save)
    try:
        pass
    except:
        print("Exception caught!")
