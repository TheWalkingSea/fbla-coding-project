from flask import Flask
import logging
from datetime import datetime


app = Flask(__name__)
dt = datetime.now()
logging.basicConfig(
    filename="./logs/app-%s.log" % dt.strftime("%Y%m%d_%H%M%S"),
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.NOTSET,
    format="%(asctime)s - %(lineno)d:%(name)s:%(levelno)s - %(message)s"
)
# conn = pgdriver.connect(dbname="postgres", user="postgres", password="postgres", host="db")


@app.route("/", methods=['GET'])
def a():
    return "Hello"
