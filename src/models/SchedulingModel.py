import ast
from database.db import get_connection
from .entities.Scheduling import Scheduling

class SchedulingModel():

    @classmethod
    def add_schedule(self, scheduling: Scheduling):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO agendamientos (id_agendamiento, id_usuario, id_estado_agendamiento, 
                               id_cita, chassis, fecha_agendamiento, visible, kilometraje, fotos, videos)  
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                               (scheduling.id, scheduling.user_id, scheduling.state, 
                                scheduling.appointment_id, scheduling.chassis_number, 
                                scheduling.date, scheduling.visible, scheduling.km, str(()), str(())))
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

                if row != None:
                    scheduling= Scheduling(row[0], row[1], row[2], row[3], row[4], row[5], row[6], 
                    ast.literal_eval(row[7]), ast.literal_eval(row[8]), 
                    row[9], row[10], row[11], row[12], row[13], row[14])
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
                    ast.literal_eval(row[7]), ast.literal_eval(row[8]), 
                    row[9], row[10], row[11], row[12], row[13], row[14])
                    schedules.append(schedule.to_JSON())             
            connection.close()
            return schedules
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_schedules_by_user_per_page(self, id, page):
        elements_per_page = 10
        offset = (int(page) - 1) * elements_per_page

        try:
            connection = get_connection()
            schedules=[]

            with connection.cursor() as cursor:
                cursor.execute("""select * from agendamientos where id_usuario=(%s) 
                               LIMIT %s OFFSET %s""",(id, elements_per_page, offset))                
                resultset = cursor.fetchall()
                
                for row in resultset:
                    schedule= Scheduling(row[0], row[1], row[2], row[3], row[4], row[5], row[6], 
                    ast.literal_eval(row[7]), ast.literal_eval(row[8]), 
                    row[9], row[10], row[11], row[12], row[13], row[14])
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
                                         ast.literal_eval(row[7]), ast.literal_eval(row[8]), row[9], 
                                         row[10], row[11], row[12], row[13], row[14])
                    schedules.append(schedule.to_JSON())             
            connection.close()
            return schedules
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_schedules_by_state_per_page(self, state, page):
        elements_per_page = 10
        offset = (int(page) - 1) * elements_per_page

        try:
            connection = get_connection()
            schedules=[]

            with connection.cursor() as cursor:
                cursor.execute("""select * from agendamientos where id_estado_agendamiento=(%s) 
                               LIMIT %s OFFSET %s""",(state, elements_per_page, offset))   
                resultset = cursor.fetchall()
                
                for row in resultset:
                    schedule= Scheduling(row[0], row[1], row[2], row[3], row[4], row[5], row[6], 
                                         ast.literal_eval(row[7]), ast.literal_eval(row[8]), row[9], 
                                         row[10], row[11], row[12], row[13], row[14])
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
                               chassis=%s, kilometraje=%s WHERE id_agendamiento = %s""", 
                               (scheduling.user_id, scheduling.state, scheduling.visible, scheduling.chassis_number, 
                                scheduling.km, scheduling.id))
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
                               kilometraje=%s, observacion=%s, costo=%s WHERE id_agendamiento = %s""", 
                               (scheduling.state, scheduling.finish_date, scheduling.return_date, 
                                scheduling.km, scheduling.details, scheduling.cost, scheduling.id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows  
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_image(self, image: str, id: str):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:

                # obtener la cadena de imagenes que se encuentra en la bd
                # convertir en formato lista para editar
                # elimino un item de la lista
                # guardo en la bd

                cursor.execute("SELECT fotos FROM agendamientos where id_agendamiento=(%s)", (id,))
                row = cursor.fetchone()
                img_names = ast.literal_eval(row[0])
                index = img_names.index(image)
                img_names.pop(index)

                cursor.execute("""UPDATE agendamientos SET fotos=%s WHERE id_agendamiento = %s""", 
                               (str(img_names), id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def add_image(self, image: str, id: str):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:

                # obtener la cadena de imagenes que se encuentra en la bd
                # convertir en formato lista para editar
                # agrego un item a la lista o reemplazo dependiendo del index
                # guardo en la bd

                cursor.execute("SELECT fotos FROM agendamientos where id_agendamiento=(%s)", (id,))
                row = cursor.fetchone()
                img_names = ast.literal_eval(row[0])  
              
                # si la celda de la bd es una tupla vacia la lista se inicializa
                if len(img_names) == 0:
                    img_names = []

                img_names.append(image)
                
                cursor.execute("""UPDATE agendamientos SET fotos=%s WHERE id_agendamiento = %s""", 
                               (str(img_names), id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_video(self, video: str, id: str):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:

                # obtener la cadena de videos que se encuentra en la bd
                # convertir en formato lista para editar
                # elimino un item de la lista
                # guardo en la bd

                cursor.execute("SELECT videos FROM agendamientos where id_agendamiento=(%s)", (id,))
                row = cursor.fetchone()
                vid_names = ast.literal_eval(row[0])
                index = vid_names.index(video)
                vid_names.pop(index)

                cursor.execute("""UPDATE agendamientos SET videos=%s WHERE id_agendamiento = %s""", 
                               (str(vid_names), id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_video(self, video: str, id: str):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:

                # obtener la cadena de videos que se encuentra en la bd
                # convertir en formato lista para editar
                # agrego un item a la lista o reemplazo dependiendo del index
                # guardo en la bd

                cursor.execute("SELECT videos FROM agendamientos where id_agendamiento=(%s)", (id,))
                row = cursor.fetchone()
                vid_names = ast.literal_eval(row[0])

                # si la celda de la bd es una tupla vacia la lista se inicializa
                if len(vid_names) == 0:
                    vid_names = []

                vid_names.append(video)

                cursor.execute("""UPDATE agendamientos SET videos=%s WHERE id_agendamiento = %s""", 
                               (str(vid_names), id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def add_document(self, document: str, id: str):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""UPDATE agendamientos SET documento_retiro=%s WHERE id_agendamiento = %s""", 
                               (document, id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows  
        except Exception as ex:
            raise Exception(ex)
