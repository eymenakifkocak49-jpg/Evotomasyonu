from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Verileri tutan değişken
ev_verileri = {"sicaklik": 0, "nem": 0, "basinc": 0}

@app.route('/guncelle', methods=['POST'])
def guncelle():
    data = request.json
    ev_verileri["sicaklik"] = data.get("sicaklik")
    ev_verileri["nem"] = data.get("nem")
    ev_verileri["basinc"] = data.get("basinc")
    return jsonify({"mesaj": "Veriler alindi"})

@app.route('/durum', methods=['GET'])
def durum():
    return jsonify(ev_verileri)

if __name__ == '__main__':
    # Render'ın istediği portu otomatik alması için bu satır şart
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
