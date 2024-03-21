from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(host="localhost", user="postgres", password="1234", dbname="nexu", port=5432)

@app.route('/brands', methods=['GET'])
def get_brands():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, average_price FROM BRANDS")
    brands = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": brand[0], "nombre": brand[1], "average_price": brand[2]} for brand in brands])

@app.route('/brands/<int:brand_id>/models', methods=['GET'])
def get_brand_models(brand_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, average_price FROM MODELS WHERE brand_name = (SELECT name FROM BRANDS WHERE id = %s)", (brand_id,))
    models = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": model[0], "name": model[1], "average_price": model[2]} for model in models])

@app.route('/brands', methods=['POST'])
def create_brand():
    name = request.json.get('name')
    if not name:
        return jsonify({'error': 'Brand name is required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO BRANDS (name) VALUES (%s) RETURNING id", (name,))
        brand_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return jsonify({'error': 'Brand name already exists'}), 409
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Brand created successfully', 'id': brand_id})

@app.route('/brands/<int:brand_id>/models', methods=['POST'])
def create_model(brand_id):
    name = request.json.get('name')
    average_price = request.json.get('average_price')

    if not name:
        return jsonify({'error': 'Model name is required'}), 400

    if average_price and average_price < 100000:
        return jsonify({'error': 'Average price must be greater than 100,000'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM BRANDS WHERE id = %s", (brand_id,))
    if cur.fetchone()[0] == 0:
        return jsonify({'error': 'Brand not found'}), 404

    try:
        cur.execute("INSERT INTO MODELS (name, average_price, brand_name) VALUES (%s, %s, (SELECT name FROM BRANDS WHERE id = %s)) RETURNING id", (name, average_price, brand_id))
        model_id = cur.fetchone()[0]
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return jsonify({'error': 'Model name already exists for this brand'}), 409
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Model created successfully', 'id': model_id})

@app.route('/models/<int:model_id>', methods=['PUT'])
def update_model(model_id):
    average_price = request.json.get('average_price')

    if not average_price:
        return jsonify({'error': 'Average price is required'}), 400

    if average_price < 100000:
        return jsonify({'error': 'Average price must be greater than 100,000'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("UPDATE MODELS SET average_price = %s WHERE id = %s", (average_price, model_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({'message': 'Model updated successfully'})

@app.route('/models', methods=['GET'])
def get_models():
    greater = request.args.get('greater')
    lower = request.args.get('lower')

    conn = get_db_connection()
    cur = conn.cursor()

    if greater and lower:
        cur.execute("SELECT id, name, average_price FROM MODELS WHERE average_price > %s AND average_price < %s", (greater, lower))
    elif greater:
        cur.execute("SELECT id, name, average_price FROM MODELS WHERE average_price > %s", (greater,))
    elif lower:
        cur.execute("SELECT id, name, average_price FROM MODELS WHERE average_price < %s", (lower,))
    else:
        cur.execute("SELECT id, name, average_price FROM MODELS")

    models = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": model[0], "name": model[1], "average_price": model[2]} for model in models])

if __name__ == '__main__':
    app.run(debug=True)