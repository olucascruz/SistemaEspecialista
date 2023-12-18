from flask import Flask, request, jsonify
from IA.main import IA
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def water_quality():
    data = request.json
    print(data)
    data = data.values()
    print(data)
    data = list(data)
    print(data)


    return jsonify(IA(data))
