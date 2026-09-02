
from flask import Flask, render_template, redirect, url_for
from forms.clientes_form import ClienteForm
from forms.productos_form import ProductoForm
from forms.proveedores_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta-semana11"


# Página principal
@app.route("/")
def inicio():

    nombre_sistema = "Sistema de Registro de Vehículos"

    return render_template(
        "index.html",
        nombre_sistema=nombre_sistema
    )

    # Datos temporales de productos/servicios
servicios_data = [
    {
        "nombre": "Estacionamiento por hora",
        "descripcion": "Servicio de estacionamiento para vehículos por hora.",
        "precio": 1.00,
        "disponible": True
    },
    {
        "nombre": "Estacionamiento por día",
        "descripcion": "Espacio de estacionamiento durante toda la jornada.",
        "precio": 8.00,
        "disponible": True
    },
    {
        "nombre": "Lavado de vehículo",
        "descripcion": "Servicio adicional de limpieza básica del vehículo.",
        "precio": 5.00,
        "disponible": False
    }
]


# Módulo Productos
@app.route("/productos", methods=["GET", "POST"])
def productos():

    form = ProductoForm()

    if form.validate_on_submit():

        nuevo_servicio = {
            "nombre": form.nombre.data,
            "descripcion": form.descripcion.data,
            "precio": float(form.precio.data),
            "disponible": form.disponible.data
        }

        servicios_data.append(nuevo_servicio)

        return redirect(url_for("productos"))

    return render_template(
        "productos.html",
        servicios=servicios_data,
        form=form
    )


# Datos temporales de clientes
clientes_data = [
    {
        "id": "001",
        "nombre": "María López",
        "cedula": "1801234567",
        "telefono": "0991234567",
        "placa": "ABC-1234"
    },
    {
        "id": "002",
        "nombre": "Juan Pérez",
        "cedula": "1802345678",
        "telefono": "0982345678",
        "placa": "XYZ-5678"
    },
    {
        "id": "003",
        "nombre": "Ana Torres",
        "cedula": "1803456789",
        "telefono": "0973456789",
        "placa": "DEF-9012"
    }
]


# Módulo Clientes
@app.route("/clientes", methods=["GET", "POST"])
def clientes():

    form = ClienteForm()

    if form.validate_on_submit():

        nuevo_cliente = {
            "id": str(len(clientes_data) + 1).zfill(3),
            "nombre": form.nombre.data,
            "cedula": form.cedula.data,
            "telefono": form.telefono.data,
            "placa": form.placa.data
        }

        clientes_data.append(nuevo_cliente)

        return redirect(url_for("clientes"))

    return render_template(
        "clientes.html",
        clientes=clientes_data,
        form=form
    )


# Módulo Proveedores

proveedores_data = [
    {
        "id": "001",
        "nombre": "Servicios de Limpieza",
        "servicio": "Productos de limpieza",
        "telefono": "0991111111"
    },
    {
        "id": "002",
        "nombre": "Mantenimiento Técnico",
        "servicio": "Mantenimiento de instalaciones",
        "telefono": "0982222222"
    },
    {
        "id": "003",
        "nombre": "Seguridad Electrónica",
        "servicio": "Cámaras y equipos de seguridad",
        "telefono": "0973333333"
    }
]


@app.route("/proveedores", methods=["GET", "POST"])
def proveedores():

    form = ProveedorForm()

    if form.validate_on_submit():

        nuevo_proveedor = {
            "id": str(len(proveedores_data) + 1).zfill(3),
            "nombre": form.nombre.data,
            "servicio": form.servicio.data,
            "telefono": form.telefono.data
        }

        proveedores_data.append(nuevo_proveedor)

        return redirect(url_for("proveedores"))

    return render_template(
        "proveedores.html",
        proveedores=proveedores_data,
        form=form
    )


# Datos temporales de facturación
facturas_data = [
    {
        "numero": "F-001",
        "cliente": "María López",
        "placa": "ABC-1234",
        "servicio": "Estacionamiento",
        "horas": 3,
        "total": 3.00
    },
    {
        "numero": "F-002",
        "cliente": "Juan Pérez",
        "placa": "XYZ-5678",
        "servicio": "Estacionamiento",
        "horas": 5,
        "total": 5.00
    },
    {
        "numero": "F-003",
        "cliente": "Ana Torres",
        "placa": "DEF-9012",
        "servicio": "Estacionamiento + Lavado",
        "horas": 2,
        "total": 7.00
    }
]


# Módulo Facturación
@app.route("/facturacion", methods=["GET", "POST"])
def facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        nueva_factura = {
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "placa": form.placa.data,
            "servicio": form.servicio.data,
            "horas": form.horas.data,
            "total": form.total.data
        }

        facturas_data.append(nueva_factura)

        return redirect(url_for("facturacion"))

    return render_template(
        "facturacion.html",
        facturas=facturas_data,
        form=form
    )


if __name__ == "__main__":
    app.run(debug=True)
