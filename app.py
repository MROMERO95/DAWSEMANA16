
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

from forms.clientes_form import ClienteForm
from forms.productos_form import ProductoForm
from forms.proveedores_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.usuario_form import UsuarioForm
from forms.login_form import LoginForm

from conexion.conexion import obtener_conexion
from models import Usuario


app = Flask(__name__)

load_dotenv()

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")


# ============================================
# CONFIGURACIÓN DE FLASK-LOGIN
# ============================================

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, usuario
        FROM usuarios
        WHERE id = %s
    """, (user_id,))

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        return Usuario(
            usuario["id"],
            usuario["usuario"]
        )

    return None


# ============================================
# PÁGINA PRINCIPAL
# ============================================

@app.route("/")
def inicio():

    nombre_sistema = "Sistema de Registro de Vehículos"

    return render_template(
        "index.html",
        nombre_sistema=nombre_sistema
    )


# ============================================
# DASHBOARD
# ============================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template("dashboard.html")


# ============================================
# REGISTRO DE USUARIO
# ============================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario_existente = cursor.fetchone()

        if usuario_existente:

            cursor.close()
            conn.close()

            return render_template(
                "registro.html",
                form=form,
                error="El nombre de usuario ya está registrado."
            )

        password_hash = generate_password_hash(
            form.password.data
        )

        cursor.execute("""
            INSERT INTO usuarios
            (usuario, password)
            VALUES (%s, %s)
        """, (
            form.usuario.data,
            password_hash
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        form=form
    )


# ============================================
# INICIAR SESIÓN
# ============================================

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario and check_password_hash(
            usuario["password"],
            form.password.data
        ):

            usuario_obj = Usuario(
                usuario["id"],
                usuario["usuario"]
            )

            login_user(usuario_obj)

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            form=form,
            error="Usuario o contraseña incorrectos."
        )

    return render_template(
        "login.html",
        form=form
    )


# ============================================
# CERRAR SESIÓN
# ============================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# ============================================
# MÓDULO PRODUCTOS
# ============================================

@app.route("/productos", methods=["GET", "POST"])
@login_required
def productos():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos
            (nombre, descripcion, precio, disponible)
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.descripcion.data,
            float(form.precio.data),
            1 if form.disponible.data else 0
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("productos"))

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM productos
    """)

    productos_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        servicios=productos_data,
        form=form
    )


# ============================================
# MODIFICAR PRODUCTO
# ============================================

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM productos
        WHERE id = %s
    """, (id,))

    producto = cursor.fetchone()

    cursor.close()
    conn.close()

    if not producto:
        return "Servicio no encontrado", 404

    form = ProductoForm()

    if request.method == "GET":

        form.nombre.data = producto["nombre"]
        form.descripcion.data = producto["descripcion"]
        form.precio.data = str(producto["precio"])
        form.disponible.data = bool(producto["disponible"])

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE productos
            SET nombre = %s,
                descripcion = %s,
                precio = %s,
                disponible = %s
            WHERE id = %s
        """, (
            form.nombre.data,
            form.descripcion.data,
            float(form.precio.data),
            1 if form.disponible.data else 0,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("productos"))

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM productos
    """)

    productos_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        servicios=productos_data,
        form=form,
        form_action=url_for("editar_producto", id=id)
    )


# ============================================
# ELIMINAR PRODUCTO
# ============================================

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM productos
        WHERE id = %s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("productos"))


# ============================================
# MÓDULO CLIENTES
# ============================================

@app.route("/clientes", methods=["GET", "POST"])
@login_required
def clientes():

    form = ClienteForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes
            (nombre, cedula, telefono, placa)
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.cedula.data,
            form.telefono.data,
            form.placa.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("clientes"))

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM clientes
    """)

    clientes_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "clientes.html",
        clientes=clientes_data,
        form=form
    )


# ============================================
# MODIFICAR CLIENTE
# ============================================

@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM clientes
        WHERE id = %s
    """, (id,))

    cliente = cursor.fetchone()

    cursor.close()
    conn.close()

    if not cliente:
        return "Cliente no encontrado", 404

    form = ClienteForm()

    if request.method == "GET":

        form.nombre.data = cliente["nombre"]
        form.cedula.data = cliente["cedula"]
        form.telefono.data = cliente["telefono"]
        form.placa.data = cliente["placa"]

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE clientes
            SET nombre = %s,
                cedula = %s,
                telefono = %s,
                placa = %s
            WHERE id = %s
        """, (
            form.nombre.data,
            form.cedula.data,
            form.telefono.data,
            form.placa.data,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("clientes"))

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM clientes
    """)

    clientes_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "clientes.html",
        clientes=clientes_data,
        form=form,
        form_action=url_for("editar_cliente", id=id)
    )


# ============================================
# ELIMINAR CLIENTE
# ============================================

@app.route("/clientes/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_cliente(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM clientes
        WHERE id = %s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("clientes"))


# ============================================
# MÓDULO PROVEEDORES
# ============================================

@app.route("/proveedores", methods=["GET", "POST"])
@login_required
def proveedores():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proveedores
            (nombre, servicio, telefono)
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.servicio.data,
            form.telefono.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("proveedores"))

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM proveedores
    """)

    proveedores_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores_data,
        form=form
    )


# ============================================
# MODIFICAR PROVEEDOR
# ============================================

@app.route("/proveedores/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM proveedores
        WHERE id = %s
    """, (id,))

    proveedor = cursor.fetchone()

    cursor.close()
    conn.close()

    if not proveedor:
        return "Proveedor no encontrado", 404

    form = ProveedorForm()

    if request.method == "GET":

        form.nombre.data = proveedor["nombre"]
        form.servicio.data = proveedor["servicio"]
        form.telefono.data = proveedor["telefono"]

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE proveedores
            SET nombre = %s,
                servicio = %s,
                telefono = %s
            WHERE id = %s
        """, (
            form.nombre.data,
            form.servicio.data,
            form.telefono.data,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("proveedores"))

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM proveedores
    """)

    proveedores_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores_data,
        form=form,
        form_action=url_for("editar_proveedor", id=id)
    )


# ============================================
# ELIMINAR PROVEEDOR
# ============================================

@app.route("/proveedores/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_proveedor(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM proveedores
        WHERE id = %s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("proveedores"))


# ============================================
# FUNCIÓN PARA LISTAR FACTURAS
# ============================================

def cargar_facturas(form, precio_hora=None):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            f.id,
            f.numero,
            c.nombre AS cliente,
            p.nombre AS producto,
            f.placa,
            f.servicio,
            p.precio,
            f.horas,
            f.total
        FROM facturacion f
        INNER JOIN clientes c
            ON f.id_cliente = c.id
        INNER JOIN productos p
            ON f.id_producto = p.id
    """)

    facturas_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "facturacion.html",
        facturas=facturas_data,
        form=form,
        precio_hora=precio_hora
    )


# ============================================
# MÓDULO FACTURACIÓN
# ============================================

@app.route("/facturacion", methods=["GET", "POST"])
@login_required
def facturacion():

    form = FacturacionForm()
    precio_hora = None

    # =========================================
    # CONSULTAR CLIENTE
    # =========================================

    if request.method == "POST" and "consultar_cliente" in request.form:

        if not form.id_cliente.data:
            return cargar_facturas(form, precio_hora)

        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, placa
            FROM clientes
            WHERE id = %s
        """, (form.id_cliente.data,))

        cliente = cursor.fetchone()

        cursor.close()
        conn.close()

        if not cliente:
            return "El cliente no existe. Verifique el ID ingresado."

        form.placa.data = cliente["placa"]

        # Mantener los datos del producto
        if form.id_producto.data:

            conn = obtener_conexion()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT id, nombre, precio
                FROM productos
                WHERE id = %s
            """, (form.id_producto.data,))

            producto = cursor.fetchone()

            cursor.close()
            conn.close()

            if producto:
                form.servicio.data = producto["nombre"]
                precio_hora = producto["precio"]

        return cargar_facturas(form, precio_hora)


    # =========================================
    # CONSULTAR PRODUCTO
    # =========================================

    if request.method == "POST" and "consultar_producto" in request.form:

        if not form.id_producto.data:
            return cargar_facturas(form, precio_hora)

        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, nombre, precio
            FROM productos
            WHERE id = %s
        """, (form.id_producto.data,))

        producto = cursor.fetchone()

        cursor.close()
        conn.close()

        if not producto:
            return "El producto no existe. Verifique el ID ingresado."

        form.servicio.data = producto["nombre"]
        precio_hora = producto["precio"]

        # Mantener los datos del cliente
        if form.id_cliente.data:

            conn = obtener_conexion()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT id, placa
                FROM clientes
                WHERE id = %s
            """, (form.id_cliente.data,))

            cliente = cursor.fetchone()

            cursor.close()
            conn.close()

            if cliente:
                form.placa.data = cliente["placa"]

        return cargar_facturas(form, precio_hora)


    # =========================================
    # CALCULAR TOTAL
    # =========================================

    if request.method == "POST" and "calcular_total" in request.form:

        if not form.id_producto.data:
            return "Primero ingrese el ID del producto y consulte el producto."

        if not form.horas.data or form.horas.data < 1:
            return "Ingrese una cantidad de horas válida."

        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, nombre, precio
            FROM productos
            WHERE id = %s
        """, (form.id_producto.data,))

        producto = cursor.fetchone()

        cursor.close()
        conn.close()

        if not producto:
            return "El producto no existe. Verifique el ID ingresado."

        form.servicio.data = producto["nombre"]

        precio_hora = producto["precio"]

        total = float(precio_hora) * form.horas.data

        form.total.data = total

        # Mantener los datos del cliente
        if form.id_cliente.data:

            conn = obtener_conexion()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT id, placa
                FROM clientes
                WHERE id = %s
            """, (form.id_cliente.data,))

            cliente = cursor.fetchone()

            cursor.close()
            conn.close()

            if cliente:
                form.placa.data = cliente["placa"]

        return cargar_facturas(form, precio_hora)


    # =========================================
    # GUARDAR FACTURA
    # =========================================

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)

        # Buscar cliente
        cursor.execute("""
            SELECT id, placa
            FROM clientes
            WHERE id = %s
        """, (form.id_cliente.data,))

        cliente = cursor.fetchone()

        if not cliente:

            cursor.close()
            conn.close()

            return "El cliente no existe. Verifique el ID ingresado."

        # Buscar producto
        cursor.execute("""
            SELECT id, nombre, precio
            FROM productos
            WHERE id = %s
        """, (form.id_producto.data,))

        producto = cursor.fetchone()

        if not producto:

            cursor.close()
            conn.close()

            return "El producto no existe. Verifique el ID ingresado."

        # Calcular total en Python
        total = float(producto["precio"]) * form.horas.data

        # Guardar factura
        cursor.execute("""
            INSERT INTO facturacion
            (
                numero,
                id_cliente,
                id_producto,
                placa,
                servicio,
                horas,
                total
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            form.numero.data,
            form.id_cliente.data,
            form.id_producto.data,
            cliente["placa"],
            producto["nombre"],
            form.horas.data,
            total
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("facturacion"))

    return cargar_facturas(form, precio_hora)

# ============================================
# MODIFICAR FACTURA
# ============================================

@app.route("/facturacion/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_factura(id):

    # =========================================
    # BUSCAR FACTURA
    # =========================================

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM facturacion
        WHERE id = %s
    """, (id,))

    factura = cursor.fetchone()

    cursor.close()
    conn.close()

    if not factura:
        return "Factura no encontrada", 404

    form = FacturacionForm()

    # =========================================
    # ACTUALIZAR FACTURA
    # =========================================

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)

        # Buscar cliente
        cursor.execute("""
            SELECT id, placa
            FROM clientes
            WHERE id = %s
        """, (form.id_cliente.data,))

        cliente = cursor.fetchone()

        if not cliente:

            cursor.close()
            conn.close()

            return "El cliente no existe. Verifique el ID ingresado."

        # Buscar producto
        cursor.execute("""
            SELECT id, nombre, precio
            FROM productos
            WHERE id = %s
        """, (form.id_producto.data,))

        producto = cursor.fetchone()

        if not producto:

            cursor.close()
            conn.close()

            return "El producto no existe. Verifique el ID ingresado."

        # Calcular total en Python
        total = float(producto["precio"]) * form.horas.data

        # Actualizar factura
        cursor.execute("""
            UPDATE facturacion
            SET numero = %s,
                id_cliente = %s,
                id_producto = %s,
                placa = %s,
                servicio = %s,
                horas = %s,
                total = %s
            WHERE id = %s
        """, (
            form.numero.data,
            form.id_cliente.data,
            form.id_producto.data,
            cliente["placa"],
            producto["nombre"],
            form.horas.data,
            total,
            id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("facturacion"))

    # =========================================
    # CARGAR DATOS EN EL FORMULARIO
    # =========================================

    form.numero.data = factura["numero"]
    form.id_cliente.data = factura["id_cliente"]
    form.id_producto.data = factura["id_producto"]
    form.placa.data = factura["placa"]
    form.servicio.data = factura["servicio"]
    form.horas.data = factura["horas"]
    form.total.data = factura["total"]

    # Obtener precio actual del producto
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT precio
        FROM productos
        WHERE id = %s
    """, (factura["id_producto"],))

    producto_edicion = cursor.fetchone()

    cursor.close()
    conn.close()

    if not producto_edicion:
        return "El producto de la factura no existe.", 404

    precio_hora = producto_edicion["precio"]

    return cargar_facturas_edicion(
        form,
        precio_hora,
        id
    )


# ============================================
# FUNCIÓN PARA LISTAR FACTURAS AL EDITAR
# ============================================

def cargar_facturas_edicion(form, precio_hora, id):

    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            f.id,
            f.numero,
            c.nombre AS cliente,
            p.nombre AS producto,
            f.placa,
            f.servicio,
            p.precio,
            f.horas,
            f.total
        FROM facturacion f
        INNER JOIN clientes c
            ON f.id_cliente = c.id
        INNER JOIN productos p
            ON f.id_producto = p.id
    """)

    facturas_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "facturacion.html",
        facturas=facturas_data,
        form=form,
        form_action=url_for("editar_factura", id=id),
        precio_hora=precio_hora
    )


# ============================================
# ELIMINAR FACTURA
# ============================================

@app.route("/facturacion/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_factura(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM facturacion
        WHERE id = %s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("facturacion"))


# ============================================
# EJECUTAR APLICACIÓN
# ============================================

if __name__ == "__main__":
    app.run(debug=True)

