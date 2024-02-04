import psycopg2

class CategoryModel:
    def __init__(self) -> None:
        self._conn = psycopg2.connect("dbname=TrabajoFinal_grupo7 user=postgres password=1234 host=localhost")
        self._cur = self._conn.cursor()
    
    def get_category(self):
        query = "SELECT id_categoria,nombre_categoria FROM categoria"
        self._cur.execute(query)
        return self._cur.fetchall()

    def create_category(self,nombre_categoria):
        query = "INSERT INTO categoria (nombre_categoria) \
            VALUES (%s)"
        self._cur.execute(query, (nombre_categoria,))
        self._conn.commit()
    
