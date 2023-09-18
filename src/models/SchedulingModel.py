from database.db import get_connection
from .entities.Scheduling import Scheduling

class SchedulingModel():

    @classmethod
    def add_schedule(self, scheduling: Scheduling):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO agendamientos (id_agendamiento, id_usuario, id_estado_agendamiento, 
                               id_cita, chassis, fecha_agendamiento, visible, fotos, videos)  
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                               (scheduling.id, scheduling.user_id, scheduling.state, 
                                scheduling.appointment_id, scheduling.chassis_number, 
                                scheduling.date, scheduling.visible, scheduling.images, scheduling.videos))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows  
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_schedule(self, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM agendamientos where id_agendamiento=(%s)", (id,))
                row = cursor.fetchone()

                appointment = None
                if row != None:
                    scheduling= Scheduling(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                             row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
                    scheduling=scheduling.to_JSON() 

            connection.close()
            return scheduling  
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_schedules_by_user(self, id):
        try:
            connection = get_connection()
            schedules=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM agendamientos where id_usuario=(%s)", (id,))
                resultset = cursor.fetchall()
                
                for row in resultset:
                    schedule= Scheduling(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                             row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
                    schedules.append(schedule.to_JSON())             
            connection.close()
            return schedules
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_schedules_by_state(self, state):
        try:
            connection = get_connection()
            schedules=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM agendamientos where id_estado_agendamiento=(%s)", (state,))
                resultset = cursor.fetchall()
                
                for row in resultset:
                    schedule= Scheduling(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                             row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])
                    schedules.append(schedule.to_JSON())             
            connection.close()
            return schedules
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_schedule(self, scheduling: Scheduling):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:                                
                cursor.execute("""UPDATE agendamientos SET id_usuario=%s, id_estado_agendamiento=%s, visible=%s, 
                               chassis=%s, fotos=%s, videos=%s WHERE id_agendamiento = %s""", 
                               (scheduling.user_id, scheduling.state, scheduling.visible, scheduling.chassis_number, 
                                scheduling.images, scheduling.videos, scheduling.id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows  
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def finish_schedule(self, scheduling: Scheduling):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:                                
                cursor.execute("""UPDATE agendamientos SET id_estado_agendamiento=%s, fecha_finalizacion=%s, fecha_retiro=%s, 
                               kilometraje=%s, observacion=%s, documento_retiro=%s, costo=%s WHERE id_agendamiento = %s""", 
                               (scheduling.state, scheduling.finish_date, scheduling.return_date, 
                                scheduling.km, scheduling.details, scheduling.document, scheduling.cost, scheduling.id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows  
        except Exception as ex:
            raise Exception(ex)