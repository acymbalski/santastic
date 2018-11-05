class person:

    code = 'z'
    name = "Default"
    family = "def"
    email = ""
    full_name = "Default Name"

    def __init__(self, code, name, family, email, full_name):
        self.code = code
        self.name = name
        self.family = family
        self.email = email
        self.full_name = full_name
        
    def __str__(self):
        return str(self.full_name)
        
    def __repr__(self):
        return str(self.full_name)