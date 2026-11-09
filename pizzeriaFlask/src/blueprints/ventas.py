from flask import Blueprint, jsonify, request
from database import mysql

ventas_bp = Blueprint('ventas', __name__, url_prefix='/api/ventas')

DIAS_MAP = {
    'domingo': 1,
    'lunes': 2,
    'martes': 3,
    'miercoles': 4,
    'jueves': 5,
    'viernes': 6,
    'sabado': 7
}

@ventas_bp.route('/dia', methods=['GET'])
def ventas_por_dia():
    dia_str = request.args.get('dia', '').lower()
    if dia_str not in DIAS_MAP:
        return jsonify({"error": "Día no válido. Use lunes, martes, etc."}), 400

    dia_num = DIAS_MAP[dia_str]
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = """
            SELECT p.id_pedido, c.nombre, p.fecha_pedido, p.total_pedido
            FROM pedido p
            JOIN clientes c ON p.id_cliente = c.id_cliente
            WHERE DAYOFWEEK(p.fecha_pedido) = %s
        """
        cursor.execute(sql, (dia_num,))
        filas = cursor.fetchall()
        
        ventas = []
        columnas = [col[0] for col in cursor.description]
        for fila in filas:
            ventas.append(dict(zip(columnas, fila)))

        total_dia = sum([v['total_pedido'] for v in ventas]) if ventas else 0

        return jsonify({
            "dia": dia_str,
            "ventas": ventas,
            "ventas_totales_dia": float(total_dia)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@ventas_bp.route('/mes', methods=['GET'])
def ventas_por_mes():
    mes = request.args.get('mes')
    anio = request.args.get('anio')

    if not mes or not anio:
        return jsonify({"error": "Debe proporcionar los parámetros mes y anio"}), 400

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = """
            SELECT p.id_pedido, c.nombre, p.fecha_pedido, p.total_pedido
            FROM pedido p
            JOIN clientes c ON p.id_cliente = c.id_cliente
            WHERE MONTH(p.fecha_pedido) = %s AND YEAR(p.fecha_pedido) = %s
        """
        cursor.execute(sql, (mes, anio))
        filas = cursor.fetchall()
        
        ventas = []
        columnas = [col[0] for col in cursor.description]
        for fila in filas:
            ventas.append(dict(zip(columnas, fila)))

        total_mes = sum([v['total_pedido'] for v in ventas]) if ventas else 0

        return jsonify({
            "mes": mes,
            "anio": anio,
            "ventas": ventas,
            "ventas_totales_mes": float(total_mes)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@ventas_bp.route('/pedidos/<int:id_pedido>/detalle', methods=['GET'])
def detalle_pedido(id_pedido):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = """
            SELECT id_detalle, tamano, ingredientes, num_pizzas, subtotal
            FROM detalle_pedido
            WHERE id_pedido = %s
        """
        cursor.execute(sql, (id_pedido,))
        filas = cursor.fetchall()
        
        detalle = []
        columnas = [col[0] for col in cursor.description]
        for fila in filas:
            detalle.append(dict(zip(columnas, fila)))

        return jsonify({
            "id_pedido": id_pedido,
            "detalle": detalle
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()