from database.db import get_connection
from .entities.User import User

class UserModel():

    @classmethod
    def login(self, user_name, password):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                #cursor.execute("SELECT id_usuario, user_name, nombre, apellido, password, id_sucursal FROM usuarios where user_name=%s and password=%s", (user_name, password))
                cursor.execute("""select id_usuario, user_name, nombre, apellido, password, s.descripcion 
                               from usuarios u, sucursal s where u.id_sucursal  = s.id_sucursal and u.user_name=%s 
                               and u.password=%s""", (user_name, password))
                row = cursor.fetchone()
                user= User(row[0], row[1], row[2], row[3], row[4], row[5])                
            connection.close()
            return user.to_JSON()    
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_users(self):
        try:
            connection = get_connection()
            users=[]

            with connection.cursor() as cursor:
                cursor.execute("""select id_usuario, nombre, apellido, user_name, password, sucursal.descripcion from usuarios, sucursal 
                               where usuarios.id_sucursal = sucursal.id_sucursal""")
                resultset = cursor.fetchall()
                
                for row in resultset:
                    user= User(row[0], row[1], row[2], row[3], None, row[5])
                    users.append(user.to_JSON())

            connection.close()
            return users    
        except Exception as ex:
            raise Exception(ex)       