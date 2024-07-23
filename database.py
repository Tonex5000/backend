import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection configuration
DB_NAME = 'soltoken'
DB_USER = 'soltoken_user'
DB_PASS = 'XxyppfV1gWfrFhmjUCwks3vU7v1yyOMp'
DB_HOST = 'dpg-cqfdrciju9rs73brac8g-a.oregon-postgres.render.com'
DB_PORT = '5432'

def setup_database():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
        )
        c = conn.cursor()

        # Create deposits table
        c.execute('''CREATE TABLE IF NOT EXISTS deposit (
            id SERIAL PRIMARY KEY,
            amount REAL,
            status TEXT,
            wallet_address TEXT
        )''')

        conn.commit()
        print("Successfully created and updated tables")
        conn.close()

    except Exception as e:
        print(f"Error during database setup: {e}")

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

def insert_deposit(wallet_address, amount, status):
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        insert_query = """
        INSERT INTO deposit (wallet_address, amount, status)
        VALUES (%s, %s, %s)
        RETURNING id, wallet_address, amount, status;
        """
        cur.execute(insert_query, (wallet_address, amount, status))
        deposit_record = cur.fetchone()
        conn.commit()
        cur.close()
        return deposit_record
    except Exception as e:
        conn.rollback()
        print(f"Error in insert_deposit: {str(e)}")
        print(f"SQL Query: {insert_query}")
        print(f"Parameters: wallet_address={wallet_address}, amount={amount}, status={status}")
        raise e
    finally:
        conn.close()

def get_total_deposited(wallet_address):
    """Get the total amount deposited by a specific wallet address."""
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        select_query = """
        SELECT SUM(amount) AS total_deposited
        FROM deposit
        WHERE wallet_address = %s;
        """
        cur.execute(select_query, (wallet_address,))
        result = cur.fetchone()
        cur.close()
        return result['total_deposited'] if result['total_deposited'] is not None else 0
    except Exception as e:
        raise e
    finally:
        conn.close()

def verify_table_exists():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM deposit LIMIT 1;")
        print("Deposit table exists and is accessible.")
        cur.close()
    except Exception as e:
        print(f"Error verifying deposit table: {str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    setup_database()
    verify_table_exists()