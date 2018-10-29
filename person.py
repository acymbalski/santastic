class person:

    code = 'z'
    name = "Default"
    family = "def"

    def __init__(self, c, n, f):
        self.code = c
        self.name = n
        self.family = f
        
    def __str__(self):
        return str(self.name)
        
    def __repr__(self):
        return str(self.name)