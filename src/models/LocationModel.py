from database.db import get_connection
from .entities.Location import Location

class LocationModel():

    @classmethod
    def get_locations(self):
        try:
            connection = get_connection()
            locations=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT id_sucursal, descripcion, direccion, telefono FROM sucursal ORDER BY id_sucursal")
                resultset = cursor.fetchall()
                
                for row in resultset:
                    local= Location(row[0], row[1], row[2], row[3])
                    locations.append(local.to_JSON())

            connection.close()
            return locations    
        except Exception as ex:
            raise Exception(ex)    