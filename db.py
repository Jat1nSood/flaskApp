import psycopg2 as pg

try : 
    conn = pg.connect(

        dbname = "postgres",
        user = "postgres",
        password = "postgres",
        host = "localhost",
        port = "5432"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT version();")

    version = cursor.fetchone()
    print("Connection Established")
    print(version)

    


except pg.Error as e:

    print("Error connecting to DB : ", e)
