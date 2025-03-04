class Appointment():
    def __init__(self, id, first_name, last_name, address, email, phone, mark, model, plate, year, location_id, mainteinance_id, date, visible:bool, document_id, user_id) -> None:
        self.id = id

        self.client_name = first_name
        self.client_last_name = last_name
        self.client_document_id = document_id
        self.client_address = address
        self.client_email = email
        self.client_phone = phone

        self.vehicle_mark = mark
        self.vehicle_model = model
        self.vehicle_plate = plate
        self.vehicle_year = year
 
        self.mainteinance_id = mainteinance_id
        self.location_id = location_id

        self.date = date
        self.visible = visible

        self.user_id = user_id
    
    def to_JSON(self):
        return {
            'id' : self.id,
            'client': {
                'name': self.client_name,
                'last_name': self.client_last_name,
                'document_id': self.client_document_id,
                'address': self.client_address,
                'email': self.client_email,
                'phone': self.client_phone,
            },

            'vehicle':{
                'mark': self.vehicle_mark,
                'model': self.vehicle_model,
                'address': self.vehicle_year,
                'plate': self.vehicle_plate,
            },

            'user_id': self.user_id, 
            'mainteinance_id': self.mainteinance_id,
            'location_id': self.location_id,
            'date': self.date,
            'visible': self.visible 
        }