from models.database_conn import DatabaseConnection

class PurchaseModel:
    def __init__(self) -> None:
        DB= DatabaseConnection()
        self._conn = DB.connection
        self._cur = DB.cursor

    def get_purchase(self):
        query = " SELECT id_orden, nombre_juego,nombre_categoria \
        FROM compra co, videojuego v, categoria c, juego_categoria jc, juego_compra jco \
        WHERE co.id_orden = jco.id_orden1 AND jco.id_juego2= v.id_juego  \
        AND v.id_juego = jc.id_juego1 AND jc.id_categoria1 = c.id_categoria \
        ORDER BY fecha_orden"
        self._cur.execute(query)
        return self._cur.fetchall()
    
    def select_purchase(self,id_orden):
        query = "SELECT precio FROM videojuego v, juego_compra jc, compra c \
        WHERE v.id_juego = jc.id_juego2 AND jc.id_orden1 = c.id_orden \
        AND id_orden = %s"
        self._cur.execute(query,(id_orden,))
        return self._cur.fetchone()     

    def close(self):
        self._cur.close()
        self._conn.close()