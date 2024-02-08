from models.database_conn import DatabaseConnection

class PurchaseModel:
    def __init__(self) -> None:
        DB= DatabaseConnection()
        self._conn = DB.connection
        self._cur = DB.cursor

    def get_products(self):
        query = " SELECT id_juego, nombre_juego,nombre_categoria \
        FROM compra co, videojuego v, categoria c, juego_categoria jc, juego_compra jco \
        WHERE co.id_orden = jco.id_orden1 AND jco.id_juego2= v.id_juego  \
        AND v.id_juego = jc.id_juego1 AND jc.id_categoria1 = c.id_categoria \
        ORDER BY fecha_orden"
        self._cur.execute(query)
        return self._cur.fetchall()
    
    def get_purchase(self):
        query = "SELECT id_orden, ciudad, fecha_orden, precio_total,nombre_cliente,nombre_juego,nombre_categoria \
                FROM cliente cl, compra co, juego_compra jc, videojuego v, juego_categoria jca, categoria c\
                WHERE c.id_categoria = jca.id_categoria1 \
                AND jca.id_juego1 = v.id_juego \
                AND v.id_juego = jc.id_juego2\
                AND jc.id_orden1 = co.id_orden\
                AND co.id_cliente1 = cl.id_cliente" 
        self._cur.execute(query)
        return self._cur.fetchall()
    
    def create_purchase(self, id_cliente, id_juego, id_categoria):
        try:
            # Realiza la inserción en la tabla de compras
            query_compra = "INSERT INTO compra (id_cliente1) VALUES (%s) RETURNING id_orden"
            self._cur.execute(query_compra, (int(id_cliente),))
            id_orden = self._cur.fetchone()[0]

            # Inserta en la tabla de juego_compra
            query_juego_compra = "INSERT INTO juego_compra (id_juego2, id_orden1) VALUES (%s, %s)"
            self._cur.execute(query_juego_compra, (int(id_juego), id_orden))

            # Inserta en la tabla de juego_categoria
            query_juego_categoria = "INSERT INTO juego_categoria (id_juego1, id_categoria1) VALUES (%s, %s)"
            self._cur.execute(query_juego_categoria, (int(id_juego), int(id_categoria)))

            self._conn.commit()

        except Exception as e:
            print("Ocurrió un error en la creación de la compra:", e)
            self.rollback()
            raise  # Re-levanta la excepción para que pueda ser manejada por el controlador


    def get_clients(self):
        query = "SELECT id_cliente, nombre_cliente FROM cliente ORDER BY nombre_cliente"
        self._cur.execute(query)
        return self._cur.fetchall()
    
    def rollback(self):
        """Revierte la transacción actual."""
        if self._conn:
            self._conn.rollback()

    def close(self):
        self._cur.close()
        self._conn.close()