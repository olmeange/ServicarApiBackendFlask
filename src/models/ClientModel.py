from database.db import get_connection
from .entities.Client import Client

class ClientModel():

    @classmethod
    def add_client(self, client: Client):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO clientes (id_cliente, nombre, apellido, direccion, telefono, email, cedula)  
                               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                               (client.id, client.first_name, client.last_name, client.address, client.phone, client.email, client.document_id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows  
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_client(self, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM clientes where id_cliente=(%s)", (id,))
                row = cursor.fetchone()

                client = None
                if row != None:
                    client= Client(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    client=client.to_JSON() 

            connection.close()
            return client  
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_clients(self):
        try:
            connection = get_connection()
            clients=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM clientes")
                resultset = cursor.fetchall()
                
                for row in resultset:
                    client= Client(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    clients.append(client.to_JSON())             
            connection.close()
            return clients
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_client(self, id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows  
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_client(self, client: Client):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""UPDATE clientes SET nombre=%s, apellido=%s, direccion=%s, telefono=%s, email=%s, cedula=%s, cod_cliente=%s 
                               WHERE id_cliente = %s""", (client.first_name, client.last_name, client.address, client.phone, client.email, 
                                                          client.document_id, client.client_code, client.id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows  
        except Exception as ex:
            raise Exception(ex)