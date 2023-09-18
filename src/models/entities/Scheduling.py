class Scheduling():
    def __init__(self, scheduling_id, user_id, scheduling_state, appointment_id:None, 
                 scheduling_date:None, visible:bool, chassis_number, images, videos, finish_date, return_date, km, details, document, cost) -> None:
        self.id = scheduling_id
        self.user_id = user_id
        self.state = scheduling_state
        self.appointment_id = appointment_id
        self.chassis_number = chassis_number
        self.date = scheduling_date
        self.visible = visible
        self.images = images
        self.videos = videos

        self.finish_date = finish_date
        self.return_date = return_date
        self.km = km
        self.details = details
        self.document = document
        self.cost = cost

    def to_JSON(self):
        return {
            'id' : self.id,
            'user_id': self.user_id,
            'state':self.state,
            'appointment_id': self.appointment_id,
            'chassis_number': self.chassis_number,
            'date': self.date, 
            'visible': self.visible,
            'images':self.images,
            'videos':self.videos,
            'finish_date': self.finish_date,
            'return_date': self.return_date,
            'km': self.km,
            'details': self.details,
            'document': self.document,
            'cost': self.cost
        }