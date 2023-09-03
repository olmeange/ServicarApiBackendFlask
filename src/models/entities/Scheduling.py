from models.entities.User import User
from models.entities.Appointment import Appointment

class Scheduling():
    def __init__(self, appointment_id, scheduling_date, scheduling_state, visible:bool, user:User, appointment: Appointment) -> None:
        self.id = appointment_id
        self.scheduling_date = scheduling_date
        self.scheduling_state = scheduling_state
        self.visible = visible

        self.user_id = user.id
        self.user_name = user.user_name
        self.user_first_name = user.first_name
        self.user_last_name = user.last_name


        self.client_name = appointment.client_name
        self.client_last_name = appointment.client_last_name
        self.client_address = appointment.client_address
        self.client_email = appointment.client_email
        self.client_phone = appointment.client_phone

        self.vehicle_mark = appointment.vehicle_mark
        self.vehicle_model = appointment.vehicle_model
        self.vehicle_year = appointment.vehicle_year
        self.vehicle_plate = appointment.vehicle_plate

        self.mainteinance_id = appointment.mainteinance_id
        self.location_id = appointment.location_id

        self.date = appointment.date
        self.visible = appointment.visible

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