from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="postgres",
        database="mydatabase",
        user="myuser",
        password="mypassword"
    )
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template("index.html", users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


"""
When use a configmap and secret, can secure the app.py

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        database=os.getenv("POSTGRES_DB", "mydatabase"),
        user=os.getenv("POSTGRES_USER", "myuser"),
        password=os.getenv("POSTGRES_PASSWORD", "mypassword")
    )
    return conn

-----or use this-------

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        database=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"]
    )
    return conn
    
==========

if want to use replica fo db connection
import random

def get_db_connection():
    hosts = ["192.168.210.171", "192.168.210.95", "192.168.210.33"]
    host = random.choice(hosts)

    conn = psycopg2.connect(
        host=host,
        database="mydatabase",
        user="myuser",
        password="mypassword"
    )
    return conn

===========

def get_db_connection():
    # Primary
    try:
        conn = psycopg2.connect(
            host="postgres_primary",
            database="mydatabase",
            user="myuser",
            password="mypassword"
        )
        return conn
    except:
        # Replica
        conn = psycopg2.connect(
            host="postgres_replica",
            database="mydatabase",
            user="myuser",
            password="mypassword"
        )
        return conn
"""
