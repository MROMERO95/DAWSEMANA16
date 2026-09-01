from flask import Flask, render_template

app = Flask(__name__)


# Página principal
@app.route("/")
def inicio():

    nombre_sistema = "Sistema de Registro de Vehículos"

    return render_template(
        "index.html",
        nombre_sistema=nombre_sistema
    )


# Módulo Productos
@app.route("/productos")
def productos():

    servicios = [
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

    return render_template(
        "productos.html",
        servicios=servicios
    )


# Módulo Clientes
@app.route("/clientes")
def clientes():

    clientes = [
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

    return render_template(
        "clientes.html",
        clientes=clientes
    )


# Módulo Proveedores
@app.route("/proveedores")
def proveedores():

    proveedores = [
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

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )


# Módulo Facturación
@app.route("/facturacion")
def facturacion():

    facturas = [
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

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


if __name__ == "__main__":
    app.run(debug=True)