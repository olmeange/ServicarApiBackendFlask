from database.db import get_connection
from .entities.Appointment import Appointment
import uuid

class AppointmentModel():

    @classmethod
    def add_appointment(self, appointment: Appointment):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:

                # pasar a model agendamiento
                # validar si existe cliente o no por cedula
                client_id = str(uuid.uuid4())
                cursor.execute("""INSERT INTO clientes (id_cliente, nombre, apellido, direccion, telefono, email, cedula)  
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (client_id, appointment.client_name, appointment.client_last_name, appointment.client_address, appointment.client_phone, appointment.client_email, appointment.client_document_id))
                affected_rows0 = cursor.rowcount
                connection.commit()

                # validar si existe vehiculo o no por chapa
                vehicle_id = str(uuid.uuid4())
                cursor.execute("""INSERT INTO vehiculos (id_vehiculo, marca, modelo, año, chapa, id_cliente)  
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (vehicle_id, appointment.vehicle_mark, appointment.vehicle_model, appointment.vehicle_year, appointment.vehicle_plate, client_id))
                affected_rows1 = cursor.rowcount
                connection.commit()

                cursor.execute("""INSERT INTO citas (id_cita, nombre_cliente, apellido_cliente, direccion_cliente, 
                               email_cliente, telefono_cliente, marca, modelo, chapa, año, id_sucursal, id_mantenimiento, fecha, visible, cedula) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                               (appointment.id, appointment.client_name, appointment.client_last_name, appointment.client_address, 
                                appointment.client_email, appointment.client_phone, appointment.vehicle_mark, appointment.vehicle_model, 
                                appointment.vehicle_plate, appointment.vehicle_year, appointment.location_id, appointment.mainteinance_id,
                                appointment.date, appointment.visible, appointment.client_document_id))
                affected_rows2 = cursor.rowcount
                connection.commit()

            connection.close()
            return [affected_rows0, affected_rows1, affected_rows2]
            #return affected_rows2  
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_appointment(self, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM citas where id_cita=(%s)", (id,))
                row = cursor.fetchone()

                appointment = None
                if row != None:
                    appointment= Appointment(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                             row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
                    appointment=appointment.to_JSON() 

            connection.close()
            return appointment  
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_appointments(self):
        try:
            connection = get_connection()
            appointments=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM citas")
                resultset = cursor.fetchall()
                
                for row in resultset:
                    appointment= Appointment(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                             row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
                    appointments.append(appointment.to_JSON())             
            connection.close()
            return appointments
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_appointments_per_page(self, page):
        elements_per_page = 10
        offset = (int(page) - 1) * elements_per_page

        try:
            connection = get_connection()
            appointments=[]

            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM citas LIMIT {elements_per_page} OFFSET {offset};')
                resultset = cursor.fetchall()
                
                for row in resultset:
                    appointment= Appointment(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                             row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
                    appointments.append(appointment.to_JSON())             
            connection.close()
            return appointments
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_appointment(self, appointment: Appointment):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:                
                cursor.execute("""UPDATE citas SET nombre_cliente=%s, apellido_cliente=%s, cedula=%s, direccion_cliente=%s, 
                               email_cliente=%s, telefono_cliente=%s, marca=%s, modelo=%s, chapa=%s, año=%s, id_sucursal=%s,
                               id_mantenimiento=%s, visible=%s WHERE id_cita = %s""", 
                               (appointment.client_name, appointment.client_last_name, appointment.client_document_id, appointment.client_address, 
                                appointment.client_email, appointment.client_phone, appointment.vehicle_mark,
                                appointment.vehicle_model, appointment.vehicle_plate, appointment.vehicle_year, 
                                appointment.location_id, appointment.mainteinance_id, appointment.visible, appointment.id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows  
        except Exception as ex:
            raise Exception(ex)