from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Global veri deposu
ev_verileri = {"sicaklik": 0, "nem": 0, "basinc": 0}

@app.route('/', methods=['GET'])
def home():
    return "Sistem Aktif."

@app.route('/guncelle', methods=['POST'])
def guncelle():
    global ev_verileri
    data = request.get_json(force=True)
    if data:
        ev_verileri["sicaklik"] = data.get("sicaklik", 0)
        ev_verileri["nem"] = data.get("nem", 0)
        ev_verileri["basinc"] = data.get("basinc", 0)
        return jsonify({"mesaj": "OK"}), 200
    return jsonify({"mesaj": "Hata"}), 400

@app.route('/durum', methods=['GET'])
def durum():
    return jsonify(ev_verileri)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
