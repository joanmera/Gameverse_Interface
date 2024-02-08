from models.database_conn import DatabaseConnection

class VideogameModel:
    def __init__(self) -> None:
     DB= DatabaseConnection()
     self._conn = DB.connection
     self._cur = DB.cursor

    def get_videogame(self):
        query = " SELECT id_juego,nombre_juego,nombre_categoria,precio,desarrollador,fecha_lanzamiento,puntuacion_general \
        FROM videojuego,juego_categoria,categoria  \
        WHERE id_juego = id_juego1  \
        AND  id_categoria = id_categoria1 \
        ORDER BY nombre_juego"
        self._cur.execute(query)
        return self._cur.fetchall()
     
    

    def create_game(self, nombre_juego, nombre_categoria, precio, desarrollador, fecha_lanzamiento, puntuacion_general):
        try:
            # Primero se inserta en videojuego
            query_videojuego = "INSERT INTO videojuego (nombre_juego, precio, desarrollador, fecha_lanzamiento, puntuacion_general) VALUES (%s, %s, %s, %s, %s) RETURNING id_juego"
            self._cur.execute(query_videojuego, (nombre_juego, precio, desarrollador, fecha_lanzamiento, puntuacion_general))
            id_juego1 = self._cur.fetchone()[0]

            # Luego se obtiene el id_categoria1 correspondiente a nombre_categoria
            query_categoria = "SELECT id_categoria FROM categoria WHERE nombre_categoria = %s"
            self._cur.execute(query_categoria, (nombre_categoria,))
            id_categoria1 = self._cur.fetchone()[0]

            # Finalmente, se inserta en juego_categoria
            query_juego_categoria = "INSERT INTO juego_categoria (id_juego1, id_categoria1) VALUES (%s, %s)"
            self._cur.execute(query_juego_categoria, (id_juego1, id_categoria1))
            self._conn.commit()

        except Exception as e:
            print("Ocurrió un error: ", e)
            return False

        return True


    def update_game(self, id_juego, nombre_juego, nombre_categoria, precio, desarrollador, fecha_lanzamiento, puntuacion_general):
        try:
            # Actualiza la información en videojuego
            query_videojuego = """
                UPDATE videojuego
                SET nombre_juego=%s, precio=%s, desarrollador=%s, fecha_lanzamiento=%s, puntuacion_general=%s
                WHERE id_juego = %s
            """
            self._cur.execute(query_videojuego, (nombre_juego, precio, desarrollador, fecha_lanzamiento, puntuacion_general, id_juego))

            # Obtiene el id_categoria correspondiente a nombre_categoria
            query_categoria = "SELECT id_categoria FROM categoria WHERE nombre_categoria = %s"
            self._cur.execute(query_categoria, (nombre_categoria,))
            id_categoria = self._cur.fetchone()[0]

            # Actualiza la relación en juego_categoria
            query_juego_categoria = """
                UPDATE juego_categoria
                SET id_categoria1 = %s
                WHERE id_juego1 = %s
            """
            self._cur.execute(query_juego_categoria, (id_categoria, id_juego))

            self._conn.commit()
            return True
        except Exception as e:
            print("Ocurrió un error: ", e)
            return False
 
    def get_game_by_id(self, game_id):
        try:
            query = """
                SELECT id_juego, nombre_juego, nombre_categoria, precio, desarrollador, fecha_lanzamiento, puntuacion_general
                FROM videojuego, juego_categoria, categoria
                WHERE id_juego = id_juego1  
                AND  id_categoria = id_categoria1 
                AND id_juego = %s
            """
            self._cur.execute(query, (game_id,))
            return self._cur.fetchone()
        except Exception as e:
            print("Ocurrió un error: ", e)
            return None
        
    def get_categories(self):
        query = "SELECT nombre_categoria FROM categoria ORDER BY nombre_categoria"
        self._cur.execute(query)
        return [result[0] for result in self._cur.fetchall()]

    def delete_game(self, game_id):
        try:
            # Elimina las filas en juego_categoria asociadas al id_juego
            query_delete_juego_categoria = "DELETE FROM juego_categoria WHERE id_juego1 = %s"
            self._cur.execute(query_delete_juego_categoria, (game_id,))

            # Elimina el juego de la tabla videojuego
            query_delete_videojuego = "DELETE FROM videojuego WHERE id_juego = %s"
            self._cur.execute(query_delete_videojuego, (game_id,))

            self._conn.commit()
            return True
        except Exception as e:
            print("Ocurrió un error al eliminar el juego: ", e)
            return False
   
 

    def rollback(self):
        """Revierte la transacción actual."""
        if self._conn:
            self._conn.rollback()

    def close(self):
        self._cur.close()
        self._conn.close()

    
   
        