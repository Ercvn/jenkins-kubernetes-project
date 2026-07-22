import os
import psycopg2
from flask import Flask

app = Flask(__name__)

# Veritabanı bağlantı fonksiyonu
def get_db_connection():
    # Değerleri Kubernetes Secret üzerinden gelen ortam değişkenlerinden alıyoruz
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME')
    )
    return conn

@app.route('/')
def hello():
    try:
        # Veritabanına bağlanıp versiyon bilgisini çekmeyi deniyoruz
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        
        return f"<h1>Merhaba Kubernetes!</h1><p>Veritabanı bağlantısı BAŞARILI: {db_version[0]}</p>"
    except Exception as e:
        return f"<h1>Hata!</h1><p>Veritabanına bağlanılamadı: {e}</p>"

if __name__ == '__main__':
    # Flask uygulamasını 5000 portunda dışarıya açıyoruz
    app.run(host='0.0.0.0', port=5000)