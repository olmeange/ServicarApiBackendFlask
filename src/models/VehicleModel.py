from database.db import get_connection
from .entities.Vehicle import Vehicle

class VehicleModel():

    @classmethod
    def add_vehicle(self, vehicle: Vehicle):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO vehiculos (id_vehiculo, marca, modelo, año, chapa, id_cliente)  
                               VALUES (%s, %s, %s, %s, %s, %s)""",
                               (vehicle.id, vehicle.mark, vehicle.model, vehicle.year, vehicle.plate, vehicle.client_id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows  
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_vehicle(self, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM vehiculos where id_vehiculo=(%s)", (id,))
                row = cursor.fetchone()

                vehicle = None
                if row != None:
                    vehicle= Vehicle(row[0], row[1], row[2], row[3], row[4], row[5])
                    vehicle=vehicle.to_JSON() 

            connection.close()
            return vehicle  
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_vehicles(self):
        try:
            connection = get_connection()
            vehicles=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM vehiculos")
                resultset = cursor.fetchall()
                
                for row in resultset:
                    vehicle= Vehicle(row[0], row[1], row[2], row[3], row[4], row[5])
                    vehicles.append(vehicle.to_JSON())             
            connection.close()
            return vehicles
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_vehicle(self, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM vehiculos WHERE id_vehiculo = %s", (id,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows  
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_vehicle(self, vehicle: Vehicle):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""UPDATE vehiculos SET marca=%s, modelo=%s, año=%s, chapa=%s 
                               WHERE id_vehiculo = %s""", (vehicle.mark, vehicle.model, vehicle.year, vehicle.plate, vehicle.id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows  
        except Exception as ex:
            raise Exception(ex)