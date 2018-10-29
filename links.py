
class link:
    source = ""
    destination = ""
    
    def __init__(self, s, d):
        self.source = s
        self.destination = d
        
    def reverse(self):
        return link(self.destination, self.source)
        
    def __str__(self):
        return str(self.source) + "->" + str(self.destination)
        
    def __repr__(self):
        return str(self.source) + "->" + str(self.destination)
        
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, link):
            return self.source == other.source and self.destination == other.destination
        return False

class linklist(list):
    links = []
    
    def __init__(self):
        #self.links = []
        pass
        
    def fromsrc(self, code):
        retlist = []
        
        for l in self:#links:
            if l.source.code == code:
                retlist.append(l)
        return retlist
        
    def todest(self, code):
        retlist = []
        
        for l in self:#links:
            if l.destination.code == code:
                retlist.append(l)
        #print("zink:")
        #print(retlist)
        return retlist
    
    # remove a list at a time
    # this will be useful for negating all of someone's links
    def rem_lis(self, remlist):
        # we need to build a temporary list because you can't
        # iterate while deleting, dummy!
        templis = []
        #print(len(self))
        #print(len(self.list))
        #print(len(links))
        for l in remlist:
            mx = len(self)#links)
            nlink = 0
            while nlink < mx:
                if l == self[nlink]:#links[nlink]:
                    self.remove(l)#links.remove(l)
                    nlink -= 1
                    mx = len(self)#links)
                nlink += 1
                    
            # for nlink in range(0, len(links)):
                # #print("{} / {}".format(nlink, len(links)))
                # if l == links[nlink]:
                    # links.remove(l)
                    # nlink -= 1
                    
        # for link in links:
            # print("ok")
            # for l in remlist:
                # if link != l:
                    # #print("keeping link:")
                    # #print(link)
                    # templis.append(link)
        # self = templis
        #links = templis
    
    def __list__(self):
        return self.links
    
    #def __getitem__(self, item):
    #    return self.links[item] # delegate to li.__getitem__
    
class chain(list):

    ch = []

    def __init__(self):
        pass
        
    def isin(self, code):
        for link in ch:
            if link.source.code == code or link.destination.code == code:
                return True
        return False
        
    def __contains__(self):
        for link in ch:
            if link.source.code == code or link.destination.code == code:
                return True
        return False
        
        
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, chain):
            for l in self.ch:
                for otherl in other:
                    if l == otherl:
                        return False
            return True
        return False
        
    def __repr__(self):
        s = ""
        s += str(self[0].source)
        for l in self:
            s += "->{}".format(str(l.destination))
        s += "\n"
        return s
        
    def __str__(self):
        s = ""
        s += str(self[0].source)
        for l in self:
            s += "->{}".format(str(l.destination))
        s += "\n"
        return s
    