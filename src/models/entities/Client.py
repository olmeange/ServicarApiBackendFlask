class Client():
    def __init__(self, id, first_name, last_name, address, phone, email, document_id, client_code=None) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.phone = phone
        self.document_id = document_id
        self.client_code = client_code
    
    def to_JSON(self):
        return {
            'id' : self.id,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'address' : self.address,
            'email' : self.email,
            'phone' : self.phone,
            'document_id': self.document_id,
            'client_code': self.client_code
        }
