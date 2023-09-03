class Location():
    def __init__(self, id, description, address, phone) -> None:
        self.id = id
        self.description = description
        self.address = address
        self.phone = phone
    
    def to_JSON(self):
        return {
            'id' : self.id,
            'description' : self.description,
            'address' : self.address,
            'phone' : self.phone,
        }