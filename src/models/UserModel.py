from database.db import get_connection
from .entities.User import User

class UserModel():

    @classmethod
    def login(self, user_name, password):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
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
    def get_user(self, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios where id_usuario=(%s)", (id,))
                #cursor.execute("""select id_usuario, user_name, nombre, apellido, password, s.descripcion 
                #               from usuarios u, sucursal s where u.id_sucursal  = s.id_sucursal 
                #               and u.id_usuario=%s""", (id))
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

    @classmethod
    def get_users_per_page(self, page):
        elements_per_page = 10
        offset = (int(page) - 1) * elements_per_page
        
        try:
            connection = get_connection()
            users=[]

            with connection.cursor() as cursor:
                cursor.execute("""select id_usuario, nombre, apellido, user_name, password, sucursal.descripcion from usuarios, sucursal where usuarios.id_sucursal = sucursal.id_sucursal 
                               LIMIT %s OFFSET %s""",(elements_per_page, offset))
                resultset = cursor.fetchall()
                
                for row in resultset:
                    user= User(row[0], row[1], row[2], row[3], None, row[5])
                    users.append(user.to_JSON())

            connection.close()
            return users    
        except Exception as ex:
            raise Exception(ex)          
        
    @classmethod
    def is_admin(self, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""select id_rol from usuarios where usuarios.id_usuario = %s""",
                               (id))
                row = cursor.fetchone()
                role = None

                if row != None:
                    role = row[0]
                
                cursor.execute("""select descripcion from roles where roles.id_rol = %s""",
                (role))
                row = cursor.fetchone()
                role_description = None

                if row != None:
                    role_description = row[0]
            connection.close()

            if role_description == 'admin':
                return True
            else:
                return False
        except Exception as ex:
            raise Exception(ex)    