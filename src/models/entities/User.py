class User():
    def __init__(self, id, user_name, first_name, last_name, password: None, location) -> None:
        self.id = id
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.location = location
    
    def to_JSON(self):
        return {
            'id' : self.id,
            'user_name' : self.user_name,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'password' : self.password,
            'location' : self.location,
        }