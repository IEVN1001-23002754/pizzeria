from flask import Blueprint, jsonify, request, current_app, flash, get_flashed_messages
from database import mysql

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/api')

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@pedidos_bp.route('/temporal', methods=['POST'])
def agregar_temporal():
    data = request.json
    tamano = data.get('tamano')
    ingredientes_lista = data.get('ingredientes', [])
    num_pizzas = int(data.get('num_pizzas', 1))

    precios_tamano = current_app.config['PRECIOS_TAMANO']
    precio_ing = current_app.config['PRECIO_INGREDIENTE']

    if tamano not in precios_tamano:
        return jsonify({"error": "Tamaño de pizza no válido"}), 400

    # Lógica de cálculo de precios
    precio_base = precios_tamano[tamano]
    costo_ingredientes = len(ingredientes_lista) * precio_ing
    subtotal = (precio_base + costo_ingredientes) * num_pizzas

    ingredientes_str = ", ".join(ingredientes_lista) if ingredientes_lista else "Sin ingredientes adicionales"

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO detalle_temporal (tamano, ingredientes, num_pizzas, subtotal) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (tamano, ingredientes_str, num_pizzas, subtotal))
        mysql.connection.commit()
        return jsonify({"mensaje": "Pizza agregada temporalmente", "subtotal": subtotal}), 201
    except Exception as e:
        if cursor:
            mysql.connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@pedidos_bp.route('/temporal', methods=['GET'])
def listar_temporal():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id_temporal, tamano, ingredientes, num_pizzas, subtotal FROM detalle_temporal")
        filas = cursor.fetchall()
        
        # Como usamos 'Cursor' estándar, convertimos las tuplas a diccionarios
        resultado = []
        columnas = [col[0] for col in cursor.description]
        for fila in filas:
            resultado.append(dict(zip(columnas, fila)))
            
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@pedidos_bp.route('/temporal/<int:id_temporal>', methods=['DELETE'])
def quitar_temporal(id_temporal):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM detalle_temporal WHERE id_temporal = %s", (id_temporal,))
        mysql.connection.commit()
        return jsonify({"mensaje": "Pizza eliminada del temporal"}), 200
    except Exception as e:
        if cursor:
            mysql.connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@pedidos_bp.route('/temporal', methods=['DELETE'])
def vaciar_temporal():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM detalle_temporal")
        mysql.connection.commit()
        return jsonify({"mensaje": "Temporal vaciado con éxito"}), 200
    except Exception as e:
        if cursor:
            mysql.connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@pedidos_bp.route('/pedidos', methods=['POST'])
def terminar_pedido():
    data = request.json
    
    # Soportamos tanto el formato de múltiples clientes como el formato individual tradicional
    clientes_data = data.get('clientes', [])
    if not clientes_data:
        # Si viene en formato individual antiguo
        clientes_data = [{
            'nombre': data.get('nombre'),
            'direccion': data.get('direccion'),
            'telefono': data.get('telefono'),
            'fecha_pedido': data.get('fecha_pedido')
        }]

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        
        cursor.execute("SELECT tamano, ingredientes, num_pizzas, subtotal FROM detalle_temporal")
        elementos_temporales = cursor.fetchall()

        if not elementos_temporales:
            return jsonify({"error": "No hay pizzas en el pedido temporal"}), 400

        total_pedido = sum([elem[3] for elem in elementos_temporales])

        # Tomamos la fecha del primer cliente o la actual para el pedido general
        fecha_pedido = clientes_data[0].get('fecha_pedido') if clientes_data else None

        # Registramos el pedido principal (asociado al primer cliente o principal)
        # Verificamos primer cliente para el id_cliente principal
        primer_c = clientes_data[0]
        cursor.execute(
            "SELECT id_cliente FROM clientes WHERE nombre = %s AND direccion = %s AND telefono = %s",
            (primer_c.get('nombre'), primer_c.get('direccion'), primer_c.get('telefono'))
        )
        cliente_db = cursor.fetchone()

        if cliente_db:
            id_cliente = cliente_db[0]
        else:
            cursor.execute(
                "INSERT INTO clientes (nombre, direccion, telefono) VALUES (%s, %s, %s)",
                (primer_c.get('nombre'), primer_c.get('direccion'), primer_c.get('telefono'))
            )
            id_cliente = cursor.lastrowid

        # Insertar pedido
        cursor.execute(
            "INSERT INTO pedido (id_cliente, fecha_pedido, total_pedido) VALUES (%s, %s, %s)",
            (id_cliente, fecha_pedido, total_pedido)
        )
        id_pedido = cursor.lastrowid

        # Registrar detalles de las pizzas
        for elem in elementos_temporales:
            cursor.execute(
                "INSERT INTO detalle_pedido (id_pedido, tamano, ingredientes, num_pizzas, subtotal) VALUES (%s, %s, %s, %s, %s)",
                (id_pedido, elem[0], elem[1], elem[2], elem[3])
            )

        # Vaciar tabla temporal
        cursor.execute("DELETE FROM detalle_temporal")
        mysql.connection.commit()

        return jsonify({
            "mensaje": "Pedido registrado exitosamente.",
            "id_pedido": id_pedido,
            "total_pedido": total_pedido
        }), 201

    except Exception as e:
        if cursor:
            mysql.connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
    data = request.json
    nombre = data.get('nombre')
    direccion = data.get('direccion')
    telefono = data.get('telefono')
    fecha_pedido = data.get('fecha_pedido')

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        
        cursor.execute("SELECT tamano, ingredientes, num_pizzas, subtotal FROM detalle_temporal")
        elementos_temporales = cursor.fetchall()

        if not elementos_temporales:
            return jsonify({"error": "No hay pizzas en el pedido temporal"}), 400

        total_pedido = sum([elem[3] for elem in elementos_temporales])

        # Verificar si el cliente ya existe
        cursor.execute(
            "SELECT id_cliente FROM clientes WHERE nombre = %s AND direccion = %s AND telefono = %s",
            (nombre, direccion, telefono)
        )
        cliente = cursor.fetchone()

        if cliente:
            id_cliente = cliente[0]
        else:
            cursor.execute(
                "INSERT INTO clientes (nombre, direccion, telefono) VALUES (%s, %s, %s)",
                (nombre, direccion, telefono)
            )
            id_cliente = cursor.lastrowid

        # Registrar pedido principal
        cursor.execute(
            "INSERT INTO pedido (id_cliente, fecha_pedido, total_pedido) VALUES (%s, %s, %s)",
            (id_cliente, fecha_pedido, total_pedido)
        )
        id_pedido = cursor.lastrowid

        # Registrar detalles
        for elem in elementos_temporales:
            cursor.execute(
                "INSERT INTO detalle_pedido (id_pedido, tamano, ingredientes, num_pizzas, subtotal) VALUES (%s, %s, %s, %s, %s)",
                (id_pedido, elem[0], elem[1], elem[2], elem[3])
            )

        # Vaciar tabla temporal
        cursor.execute("DELETE FROM detalle_temporal")
        mysql.connection.commit()

        flash(f"Pedido registrado exitosamente. Importe total a pagar: ${total_pedido:.2f}")
        mensajes = get_flashed_messages()
        mensaje_flash = mensajes[0] if mensajes else ""

        return jsonify({
            "mensaje": mensaje_flash,
            "id_pedido": id_pedido,
            "total_pedido": total_pedido
        }), 201

    except Exception as e:
        if cursor:
            mysql.connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()