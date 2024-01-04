from flask import Flask
import psycopg2 as pgdriver

app = Flask(__name__)
conn = pgdriver.connect(dbname="postgres", user="postgres", password="postgres", host="db")


@app.route("/", methods=['GET'])
def a():
    return "Hello"
