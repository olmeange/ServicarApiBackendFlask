from database.db import get_connection
from .entities.Maintenance import Maintenance

class MaintenanceModel():

    @classmethod
    def get_maintenances(self):
        try:
            connection = get_connection()
            maintenances=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT id_mantenimiento, descripcion FROM mantenimientos ORDER BY id_mantenimiento")
                resultset = cursor.fetchall()
                
                for row in resultset:
                    maintenance= Maintenance(row[0], row[1])
                    maintenances.append(maintenance.to_JSON())

            connection.close()
            return maintenances    
        except Exception as ex:
            raise Exception(ex)    