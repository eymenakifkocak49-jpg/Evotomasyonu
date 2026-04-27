from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Verileri tutan değişken
ev_verileri = {"sicaklik": 0, "nem": 0, "basinc": 0}

@app.route('/')
def home():
    return "Ev Otomasyonu Sunucusu Aktif! Sistem çalışıyor."

@app.route('/guncelle', methods=['POST'])
def guncelle():
    data = request.get_json() # 'request.json' yerine bu daha garantidir
    if data:
        ev_verileri["sicaklik"] = data.get("sicaklik", 0)
        ev_verileri["nem"] = data.get("nem", 0)
        ev_verileri["basinc"] = data.get("basinc", 0)
        return jsonify({"mesaj": "Veriler alindi"}), 200
    return jsonify({"hata": "Veri gonderilmedi"}), 400

@app.route('/durum', methods=['GET'])
def durum():
    return jsonify(ev_verileri)

if __name__ == '__main__':
    # Burası lokal test için iyidir, Render'da Gunicorn zaten bunu yönetir
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host='0.0.0.0', port=port)
    
