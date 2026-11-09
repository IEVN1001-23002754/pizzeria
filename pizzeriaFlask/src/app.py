from flask import Flask
from flask_cors import CORS
from config import config
from database import mysql
from blueprints.pedidos import pedidos_bp
from blueprints.ventas import ventas_bp

app = Flask(__name__)
app.config.from_object(config['development'])

app.config['PRECIOS_TAMANO'] = {
    'Chica': 40,
    'Mediana': 80,
    'Grande': 120
}
app.config['PRECIO_INGREDIENTE'] = 10 

CORS(app)
mysql.init_app(app)

app.register_blueprint(pedidos_bp)
app.register_blueprint(ventas_bp)

@app.route('/')
def index():
    return "API REST de Pizzería activa y funcionando."

if __name__ == '__main__':
    app.run(debug=True, port=5000)