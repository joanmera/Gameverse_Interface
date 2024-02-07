import psycopg2

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection,cls).__new__(cls)

            try:
                cls._instance._conn = psycopg2.connect("dbname=trabajoFinal_grupo7 user=postgres password=1234 host=localhost")
                cls._instance._cur = cls._instance._conn.cursor()
            except Exception as e:
                print(f"Error al conectar con la DB: {e}")
                raise e
            
        return cls._instance
    
    @property
    def cursor(self):
        return self._instance._cur
    
    @property
    def connection(self):
        return self._instance._conn
    
