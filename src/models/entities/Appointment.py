class Appointment():
    def __init__(self, id, first_name, last_name, address, email, phone, mark, model, year, plate, location_id, mainteinance_id, date, visible:bool) -> None:
        self.id = id

        self.client_name = first_name
        self.client_last_name = last_name
        self.client_address = address
        self.client_email = email
        self.client_phone = phone

        self.vehicle_mark = mark
        self.vehicle_model = model
        self.vehicle_year = year
        self.vehicle_plate = plate

        self.mainteinance_id = mainteinance_id
        self.location_id = location_id

        self.date = date
        self.visible = visible
    
    def to_JSON(self):
        return {
            'id' : self.id,
            'client': {
                'name': self.client_name,
                'last_name': self.client_last_name,
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

            'mainteinance_id': self.mainteinance_id,
            'location_id': self.location_id,
            'date': self.date,
            'visible': self.visible 
        }