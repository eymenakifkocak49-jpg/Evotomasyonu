from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import os
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

VERI_DOSYASI = "/tmp/ev_verileri.json"

def veri_oku():
    try:
        if os.path.exists(VERI_DOSYASI):
            with open(VERI_DOSYASI, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Veri okuma hatasi: {e}")
    return {"sicaklik": 0, "nem": 0, "basinc": 0}

def veri_yaz(data):
    try:
        with open(VERI_DOSYASI, "w") as f:
            json.dump(data, f)
        return True
    except Exception as e:
        print(f"Veri yazma hatasi: {e}")
        return False

@app.route('/')
def home():
    return "Sistem Aktif."

@app.route('/durum', methods=['GET'])
def durum():
    return jsonify(veri_oku())

@app.route('/guncelle', methods=['POST'])
def guncelle():
    data = request.get_json(force=True)
    if data:
        mevcut_veri = veri_oku()
        mevcut_veri["sicaklik"] = data.get("sicaklik", 0)
        mevcut_veri["nem"] = data.get("nem", 0)
        mevcut_veri["basinc"] = data.get("basinc", 0)
        if veri_yaz(mevcut_veri):
            socketio.emit('veri', mevcut_veri)
            return jsonify({"durum": "basarili"}), 200
        else:
            return jsonify({"hata": "Dosyaya yazılamadı"}), 500
    return jsonify({"hata": "Veri yok"}), 400

@socketio.on('connect')
def connect():
    socketio.emit('veri', veri_oku())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
