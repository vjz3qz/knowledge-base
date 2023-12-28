import psycopg2

def get_db_connection():
    return psycopg2.connect("dbname=yourdbname user=yourusername password=yourpassword")

def execute_query(query, params):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
