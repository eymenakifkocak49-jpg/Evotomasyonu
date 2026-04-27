from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

# Verileri tutan dosya yolu
VERI_DOSYASI = "/tmp/ev_verileri.json"

def veri_oku():
    """JSON dosyasından verileri oku"""
    try:
        if os.path.exists(VERI_DOSYASI):
            with open(VERI_DOSYASI, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Veri okuma hatasi: {e}")
    return {"sicaklik": 0, "nem": 0, "basinc": 0}

def veri_yaz(data):
    """Verileri JSON dosyasına yaz"""
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

@app.route('/guncelle', methods=['POST', 'GET'])
def guncelle():
    data = request.get_json(force=True)
    if data:
        print(f"Sunucuya gelen veri: {data}")

        mevcut_veri = veri_oku()
        mevcut_veri["sicaklik"] = data.get("sicaklik", 0)
        mevcut_veri["nem"] = data.get("nem", 0)
        mevcut_veri["basinc"] = data.get("basinc", 0)

        if veri_yaz(mevcut_veri):
            return jsonify({"durum": "basarili"}), 200
        else:
            return jsonify({"hata": "Dosyaya yazılamadı"}), 500

    return jsonify({"hata": "Veri yok"}), 400

@app.route('/durum', methods=['GET'])
def durum():
    return jsonify(veri_oku())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
