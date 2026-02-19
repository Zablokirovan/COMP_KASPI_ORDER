import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()

db_client = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

def get_info_in_db(telegram_id):
    """

    :param telegram_id:
    :return:
    """
    with db_client.cursor() as cur:
        cur.execute(f"""
        SELECT
        COALESCE(s.state, '') AS state,
        (s.tg_id IS NOT NULL) AS found
        FROM (
        SELECT tg_id, state
        FROM "Kaspi".tg_driver_state
        WHERE tg_id =%s
        LIMIT 1
        ) s
        RIGHT JOIN (SELECT 1) dummy ON TRUE;""", (telegram_id,))

        return cur.fetchone()

