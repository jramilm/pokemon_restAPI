from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "pokemon_db"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route('/')
def hello_world():
    return "<h1>Hello World!</h1>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/api/pokemon", methods=['GET'])
def get_pokemon():
    data = data_fetch("SELECT * FROM pokemon")
    return make_response(jsonify(data), 200)


if __name__ == '__main__':
    app.run(debug=True)