#!/usr/bin/python3

import random
import json
import argparse
import pickle

from person import person
from links import link, linklist, chain

import EmailioEstevez
     

class santastic():     

    people = []

    emailer = None
    send_enabled = False
    
    def __init__(self, email_cfg="", actually_send=False):
        self.send_enabled = actually_send
        if self.send_enabled:
            self.emailer = EmailioEstevez.Emailio(email_cfg)
        else:
            self.emailer = EmailioEstevez.Emailio()

        
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

    def send_all_emails(self, chain):
        # get person
        for link in chain:
            self.send_email(link)
            self.emailer.clear_addresses()
    
    def send_email(self, link):
        # from -> to
        person = link.source
        giftee = link.destination
        
        # build subject/message
        self.emailer.add_address(person.email)
        
        self.emailer.set_subject("Secret Santa Pick")
        self.emailer.set_message_with_template("secret_santa_template.txt", [person.full_name, giftee.full_name])
        
        # send
        if self.send_enabled:
            print("Actually sending email to {}...".format(person.name))
            self.emailer.send()
        else:
            print("Not actually sending email.")
        #self.emailer.send()
    
    def resend(self, chain):
        # iterate list
        index = 0
        for person in self.people:
            print("{}: {}".format(str(index), person))
            index += 1
        
        validChoice = False
        print()
        while not validChoice:
            print("Select target(s) to resend, following this format (ex): 1,4,5")
            choices = input()
            
            try:
                for choice in choices.split(','):
                    index = int(choice.strip())
                    print("Sending email for person: {}...".format(self.people[index]))
                    
                    for link in chain:
                        if link.source.code == self.people[index].code:
                            self.send_email(link)
                            self.emailer.clear_addresses()
                            break
                    
                    
                validChoice = True
            except:
                print("Invalid choice. Try again.")
        # ask user to select numbers
        # send()
        
    def cleanup(self):
        print()
        print("Cleaning up...")
        self.emailer.close()

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, help="family config file")
    parser.add_argument("-l", "--load", type=str, help="load saved chain filename")
    parser.add_argument("-o", "--save", type=str, help="save chain filename (default: secret.santa)", default="secret.santa")
    parser.add_argument("-e", "--email_config", type=str, help="email config file")
    parser.add_argument("-A", "--actually_send", action="store_true", help="will not actually send emails without this")
    parser.add_argument("-r", "--resend", action="store_true", help="launch email re-sender")


    args = parser.parse_args()
    
    try:
        santa = santastic(args.email_config, args.actually_send)
    
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
        
        if args.resend:
            santa.resend(ch)
        
        if args.actually_send:
            if not args.resend:
                santa.send_all_emails(ch)

    except:
        print("Exception caught!")
    finally:
        if args.actually_send:
            santa.cleanup()
