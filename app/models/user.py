class User:
    def __init__(self,id,username,display_name,email=None):
        self.id = id
        self.username = username
        self.display_name = display_name
        self.email = email