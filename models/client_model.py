import psycopg2

class ClientModel:
    def __init__(self) -> None:
        self._conn = psycopg2.connect("dbname=TrabajoFinal_grupo7 user=postgres password=1234 host=localhost")
        self._cur = self._conn.cursor()

    def get_clients(self):
        query = "SELECT * FROM cliente ORDER BY nombre_cliente"
        self._cur.execute(query)
        return self._cur.fetchall()
    
    def create_client(self, cedula,nombre_cliente,edad,genero,telefono):
        query = "INSERT INTO cliente (cedula,nombre_cliente,edad, genero, telefono) VALUES (%s, %s, %s,%s,%s)"
        self._cur.execute(query, (cedula,nombre_cliente,edad,genero,telefono))
        self._conn.commit()

    def update_client(self,id_cliente, cedula,nombre_cliente,edad,genero,telefono):
        try:
                query = "UPDATE cliente SET cedula=%s,nombre_cliente=%s,edad=%s,genero=%s,telefono=%s WHERE id_cliente=%s"
                self._cur.execute(query, (cedula,nombre_cliente,edad,genero,telefono, id_cliente))
                self._conn.commit()
                return True
        except Exception as e:
            print("Ocurrió un error: ", e)
            return False
        
    def get_client_by_id(self, client_id):
        
        try:
                query = "SELECT * FROM cliente WHERE id_cliente =%s "
                self._cur.execute(query, (client_id,))
                return self._cur.fetchone()
            
        except Exception as e:
            print("Ocurrió un error: ", e)
            return None

    def delete_client(self, client_id):
        try:
            query = "DELETE FROM cliente WHERE id_cliente = %s"
            self._cur.execute(query, (client_id,))
            self._conn.commit()
            return True
        except Exception as e:
            print("Ocurrió un error al eliminar al estudiante: ", e)
            return False        

    def close(self):
        self._cur.close()
        self._conn.close()



''''
    def update_client(self, nombre_cliente,cedula,genero,telefono):
        try:
                query = "UPDATE cliente SET nombre_cliente=%s, cedula=%s, genero=%s, telefono=%s WHERE id_cliente=%s"
                self._cur.execute(query, (nombre_cliente,cedula,genero,telefono))
                self._conn.commit()
                return True
                 
        except Exception as e:
            print("Ocurrió un error: ", e)
            return False
    

    def close(self):
            self._cur.close()
            self._conn.close()
'''