import psycopg2

class ClientModel:
    def __init__(self) -> None:
        self._conn = psycopg2.connect("dbname=TrabajoFinal_grupo7 user=postgres password=1234 host=localhost")
        self._cur = self._conn.cursor()

    def get_students(self):
        query = "SELECT * FROM cliente ORDER BY nombre_cliente"
        self._cur.execute(query)
        return self._cur.fetchall()
    

   
