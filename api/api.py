from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    try:
        with open('../data/data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501, debug=True)
