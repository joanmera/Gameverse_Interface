from models.database_conn import DatabaseConnection

class PurchaseModel:
    def __init__(self) -> None:
        DB= DatabaseConnection()
        self._conn = DB.connection
        self._cur = DB.cursor

    def get_products(self):
        query = " SELECT id_juego, nombre_juego,nombre_categoria \
        FROM videojuego v, categoria c, juego_categoria jc \
        WHERE v.id_juego = jc.id_juego1 AND jc.id_categoria1 = c.id_categoria \
        "
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
    
    def create_purchase(self, id_cliente, fecha_orden, id_juegos,precio_total):
        try:
            # Realiza la inserción en la tabla de compras
            query_compra = "INSERT INTO compra (id_cliente1, fecha_orden,precio_total) VALUES (%s, %s,%s) RETURNING id_orden"
            self._cur.execute(query_compra, (id_cliente, fecha_orden,precio_total),)
            id_orden = self._cur.fetchone()[0]  # Obtener el ID de la orden recién insertada

            # Asocia los juegos a la compra en la tabla juego_compra
            query_juego_compra = "INSERT INTO juego_compra (id_orden1, id_juego2) VALUES (%s, %s)"
            for id_juego in id_juegos:
                self._cur.execute(query_juego_compra, (id_orden, id_juego),)

            self._conn.commit()

        except Exception as e:
            print("Ocurrió un error en la creación de la compra:", e)
            self.rollback()
            raise  # Re-levanta la excepción para que pueda ser manejada por el controlador

    def get_total(self, id_juego):
        query = "SELECT precio FROM videojuego WHERE id_juego = %s"
        self._cur.execute(query, (id_juego,))
        result = self._cur.fetchone()
        if result:
            return float(result[0])  # Convertir a float antes de devolver
        else:
            return 0.0  # O un valor predeterminado si el precio no está disponible



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