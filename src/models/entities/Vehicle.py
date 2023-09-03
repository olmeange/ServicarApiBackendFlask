class Vehicle():
    def __init__(self, id, mark, model, year, plate, client_id: None) -> None:
        self.id = id
        self.mark = mark
        self.model = model
        self.year = year
        self.plate = plate
        self.client_id = client_id
    
    def to_JSON(self):
        return {
            'id' : self.id,
            'mark' : self.mark,
            'model' : self.model,
            'year' : self.year,
            'plate' : self.plate,
            'client_id' : self.client_id
        }