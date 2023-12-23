from flask import Flask, make_response, jsonify, request
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


@app.route("/api/pokemon/<int:pok_id>", methods=['GET'])
def get_pokemon_by_id(pok_id):
    data = data_fetch("SELECT * FROM pokemon WHERE pok_id = {}".format(pok_id))

    return make_response(jsonify(data), 200)


@app.route("/api/pokemon/<string:pok_name>", methods=['GET'])
def get_pokemon_by_name(pok_name):
    data = data_fetch("SELECT * FROM pokemon WHERE pok_name = '{}'".format(pok_name))

    return make_response(jsonify(data), 200)


@app.route("/api/pokemon/type", methods=['GET'])
def get_all_types():
    data = data_fetch("SELECT type_name FROM types")

    return make_response(jsonify(data), 200)


@app.route("/api/pokemon/type/<string:type_name>", methods=['GET'])
def get_pokemon_by_type(type_name):
    query = """
           SELECT pt.pok_id, p.pok_name, t.type_name 
           FROM pokemon_types pt
           INNER JOIN pokemon p ON pt.pok_id = p.pok_id
           INNER JOIN types t ON pt.type_id = t.type_id
           WHERE t.type_name = '{}'
       """.format(type_name)
    data = data_fetch(query)

    return make_response(jsonify(data), 200)


@app.route("/api/pokemon/ability", methods=['GET'])
def get_pokemon_abilities():
    query = "SELECT abil_name FROM abilities"
    data = data_fetch(query)

    return make_response(jsonify(data), 200)


@app.route("/api/pokemon/ability/<string:abil_name>", methods=['GET'])
def get_pokemon_by_ability(abil_name):
    query = """
        SELECT pa.pok_id, p.pok_name, ab.abil_name, pa.is_hidden, pa.slot
        FROM pokemon_abilities pa 
        INNER JOIN pokemon p ON pa.pok_id = p.pok_id
        INNER JOIN abilities ab ON pa.abil_id = ab.abil_id
        WHERE ab.abil_name = '{}'
    """.format(abil_name)
    data = data_fetch(query)

    return make_response(jsonify(data), 200)


@app.route("/api/pokemon", methods=['POST'])
def add_pokemon():
    if request.is_json:
        data = request.get_json()
        pok_name = data.get('pok_name')
        pok_height = data.get('pok_height')
        pok_weight = data.get('pok_weight')
        pok_base_experience = data.get('pok_base_experience')

        query = f"INSERT INTO pokemon VALUES (0, '{pok_name}', {pok_height}, {pok_weight}, {pok_base_experience})"
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()

        return make_response(jsonify({"message": "Pokemon added successfully"}), 201)
    else:
        return make_response(jsonify({"error": "Invalid JSON data"}), 400)


if __name__ == '__main__':
    app.run(debug=True)