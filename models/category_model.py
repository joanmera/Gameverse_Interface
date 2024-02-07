from models.database_conn import DatabaseConnection

class CategoryModel:
    def __init__(self) -> None:
        DB= DatabaseConnection()
        self._conn = DB.connection
        self._cur = DB.cursor
    
    def get_category(self):
        query = "SELECT id_categoria,nombre_categoria FROM categoria"
        self._cur.execute(query)
        return self._cur.fetchall()

    def create_category(self,nombre_categoria):
        query = "INSERT INTO categoria (nombre_categoria) \
            VALUES (%s)"
        self._cur.execute(query, (nombre_categoria,))
        self._conn.commit()

    def update_category(self,id_categoria,nombre_categoria):
        try:
                query = "UPDATE categoria SET nombre_categoria = %s WHERE id_categoria=%s"
                self._cur.execute(query, (nombre_categoria,id_categoria))
                self._conn.commit()
                return True
        except Exception as e:
            print("Ocurrió un error: ", e)
            return False

    def get_category_by_id(self,id_categoria):
        try:
            query="SELECT * FROM categoria WHERE id_categoria = %s"
            self._cur.execute(query,(id_categoria,))
            return self._cur.fetchone()
        except Exception as e:
            print("Ocurrió un error: ", e)
            return None
    
    def delete_category(self, id_categoria):
        try:
            query = "DELETE FROM categoria WHERE id_categoria = %s"
            self._cur.execute(query, (id_categoria,))
            self._conn.commit()
            return True
        except Exception as e:
            print("Ocurrió un error al eliminar categoria: ", e)
            return False
        
    def close(self):
        self._cur.close()
        self._conn.close()
