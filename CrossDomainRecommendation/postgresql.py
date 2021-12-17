DB_HOST = 'songuser.cxvgpodissyo.ap-south-1.rds.amazonaws.com'
DB_NAME = 'songuser'
DB_USER = 'CrossDomain'
DB_PASS = 'wIOcAL4Rn7y2BNeexpLW'

import psycopg2

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=5432, sslmode='require')

with conn:
    crsr = conn.cursor()


    # sqlcommand = """CREATE TA