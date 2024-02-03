import psycopg2

class CategoryModel:
    def __init__(self) -> None:
        self._conn = psycopg2.connect("dbname=TrabajoFinal_grupo7 user=postgres password=1234 host=localhost")
        self._cur = self._conn.cursor()
    
    def get_category(self):
        query = "SELECT id_categoria,nombre_categoria,nombre_juego \
            FROM categoria c, videojuego v, juego_categoria jc \
            WHERE v.id_juego = jc.id_juego1 AND jc.id_categoria1 = c.id_categoria"
        self._cur.execute(query)
        return self._cur.fetchall()