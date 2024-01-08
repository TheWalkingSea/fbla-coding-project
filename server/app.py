from flask import Flask, request, jsonify, Response
import logging
from datetime import datetime
from db.adapter import DatabaseAdapter
import models.partner

app = Flask(__name__)
dt = datetime.now()
logging.basicConfig(
    filename="./logs/app-%s.log" % dt.strftime("%Y%m%d_%H%M%S"),
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.NOTSET,
    format="%(asctime)s - %(lineno)d:%(name)s:%(levelno)s - %(message)s"
)
db_params = {
    "dbname": "postgres", 
    "user": "postgres", 
    "password": "postgress", 
    "host": "db"}
adapter = DatabaseAdapter(conn=None, **db_params)
adapter.connect()

@app.route("/api/v1/partner/", methods=["POST"])
def create_partner():
    js = request.json
    models.partner.Partner.build_partner(adapter.conn, **js)
    return Response(status=200)

@app.route("/api/v1/partner/<partner_pk>", methods=["GET", "DELETE", "PUT"])
def partner(partner_pk):
    partner = models.partner.Partner(partner_pk, adapter.conn)
    if (request.method == "GET"):
        print("Aba")
        data = partner.getFields()
        logging.info(f"GET data for partner_pk: {partner_pk}; {data}")
        return jsonify(data)
    elif (request.method == "DELETE"):
        partner.deleteRecord()
    elif (request.method == "PUT"):
        pass
    return Response(status=200)

@app.route("/", methods=['GET'])
def a():
    return "Hello"

