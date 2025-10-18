from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_NAME = os.getenv("POSTGRES_DB", "testdb")

def get_db_version():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        cur.close()
        conn.close()
        return version[0]
    except Exception as e:
        return str(e)

@app.route("/")
def home():
    return jsonify({"message": "Flask API is running", "db_version": get_db_version()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)