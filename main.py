from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
from dicttoxml import dicttoxml

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

    formatted_data = format_output(data)
    return make_response(formatted_data, 200)


@app.route("/api/pokemon/<int:pok_id>", methods=['GET'])
def get_pokemon_by_id(pok_id):
    query = """
        SELECT 
            p.pok_id,
            p.pok_name,
            p.pok_height,
            p.pok_weight,
            p.pok_base_experience,
            t.type_name,
            ab.abil_name,
            pa.is_hidden,
            pa.slot
        FROM pokemon p
        INNER JOIN pokemon_types pt ON p.pok_id = pt.pok_id
        INNER JOIN types t ON pt.type_id = t.type_id
        INNER JOIN pokemon_abilities pa ON p.pok_id = pa.pok_id
        INNER JOIN abilities ab ON pa.abil_id = ab.abil_id
        WHERE p.pok_id = {}
    """.format(pok_id)
    data = data_fetch(query)

    formatted_data = format_output(data)
    return make_response(formatted_data, 200)


@app.route("/api/pokemon/<string:pok_name>", methods=['GET'])
def get_pokemon_by_name(pok_name):
    query = """
            SELECT 
                p.pok_id,
                p.pok_name,
                p.pok_height,
                p.pok_weight,
                p.pok_base_experience,
                t.type_name,
                ab.abil_name,
                pa.is_hidden,
                pa.slot
            FROM pokemon p
            INNER JOIN pokemon_types pt ON p.pok_id = pt.pok_id
            INNER JOIN types t ON pt.type_id = t.type_id
            INNER JOIN pokemon_abilities pa ON p.pok_id = pa.pok_id
            INNER JOIN abilities ab ON pa.abil_id = ab.abil_id
            WHERE p.pok_name = '{}'
        """.format(pok_name)
    data = data_fetch(query)

    formatted_data = format_output(data)
    return make_response(formatted_data, 200)


@app.route("/api/pokemon/type", methods=['GET'])
def get_all_types():
    data = data_fetch("SELECT type_name FROM types")

    formatted_data = format_output(data)
    return make_response(formatted_data, 200)


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

    formatted_data = format_output(data)
    return make_response(formatted_data, 200)


@app.route("/api/pokemon/ability", methods=['GET'])
def get_pokemon_abilities():
    query = "SELECT abil_name FROM abilities"
    data = data_fetch(query)

    formatted_data = format_output(data)
    return make_response(formatted_data, 200)


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

    formatted_data = format_output(data)
    return make_response(formatted_data, 200)


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


@app.route("/api/pokemon/<int:pok_id>", methods=['PUT'])
def update_pokemon(pok_id):
    if request.is_json:
        data = request.get_json()
        pok_name = data.get('pok_name')
        pok_height = data.get('pok_height')
        pok_weight = data.get('pok_weight')
        pok_base_experience = data.get('pok_base_experience')

        query = f"""
            UPDATE pokemon 
            SET pok_name = '{pok_name}', pok_height = {pok_height}, pok_weight = {pok_weight}, pok_base_experience = {pok_base_experience}
            WHERE pok_id = {pok_id}
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        rows_affected = cur.rowcount
        cur.close()

        return make_response(jsonify({"message": "Pokemon updated successfully", "rows_affected": rows_affected}), 200)
    else:
        return make_response(jsonify({"error": "Invalid JSON data"}), 400)


@app.route("/api/pokemon/<int:pok_id>", methods=["DELETE"])
def delete_pokemon(pok_id):
    cur = mysql.connection.cursor()

    # Check if the Pokemon exists before attempting to delete
    exists_query = "SELECT * FROM pokemon WHERE pok_id = {}".format(pok_id)
    cur.execute(exists_query)
    if not cur.fetchone():
        cur.close()
        return make_response(jsonify({"error": "Pokemon not found"}), 404)

    delete_query = "DELETE FROM pokemon WHERE pok_id = {}".format(pok_id)
    cur.execute(delete_query)
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()

    if rows_affected > 0:
        return make_response(jsonify({"message": "Pokemon deleted successfully", "rows_affected": rows_affected}), 200)
    else:
        # If no rows were affected, it means the specified pok_id was not found
        return make_response(jsonify({"error": "Pokemon not found"}), 404)


def format_output(data):
    output_format = request.args.get("format", "json").lower()

    if output_format == "json":
        return jsonify(data)
    elif output_format == "xml":
        xml_data = dicttoxml(data)
        return make_response(xml_data, 200, {"Content-Type": "application/xml"})
    else:
        return make_response(jsonify({"error": "Invalid format specified"}), 400)


if __name__ == '__main__':
    app.run(debug=True)