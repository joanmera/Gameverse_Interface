import psycopg2

class PurchaseModel:
    def __init__(self) -> None:
        self._conn = psycopg2.connect("dbname=trabajoFinal_grupo7 user=postgres password=1234 host=localhost")
        self._cur = self._conn.cursor()

    def get_purchase(self):
        query = " SELECT id_orden, nombre_juego,nombre_categoria \
  FROM compra co, videojuego v, categoria c, juego_categoria jc, juego_compra jco \
  WHERE co.id_orden = jco.id_orden1 AND jco.id_juego2= v.id_juego  \
  AND v.id_juego = jc.id_juego1 AND jc.id_categoria1 = c.id_categoria"
        self._cur.execute(query)
        return self._cur.fetchall()
    
    def close(self):
        self._cur.close()
        self._conn.close()