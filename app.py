from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Global değişken
ev_verileri = {"sicaklik": 0, "nem": 0, "basinc": 0}

@app.route('/guncelle', methods=['POST'])
def guncelle():
    global ev_verileri  # BU SATIR EN ÖNEMLİSİ!
    data = request.get_json(force=True)
    if data:
        ev_verileri["sicaklik"] = data.get("sicaklik", 0)
        ev_verileri["nem"] = data.get("nem", 0)
        ev_verileri["basinc"] = data.get("basinc", 0)
        print(f"Guncellendi: {ev_verileri}") # Loglarda bunu görmelisin
        return jsonify({"mesaj": "OK"}), 200
    return jsonify({"mesaj": "Veri yok"}), 400

@app.route('/durum', methods=['GET'])
def durum():
    return jsonify(ev_verileri)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
