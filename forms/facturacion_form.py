from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class FacturacionForm(FlaskForm):

    numero = StringField(
        "Número de factura",
        validators=[
            DataRequired(
                message="El número de factura es obligatorio."
            ),
            Length(
                min=5,
                max=10,
                message="El número de factura debe tener entre 5 y 10 caracteres."
            )
        ]
    )

    id_cliente = IntegerField(
        "ID del cliente",
        validators=[
            DataRequired(
                message="El ID del cliente es obligatorio."
            ),
            NumberRange(
                min=1,
                message="El ID del cliente debe ser mayor que 0."
            )
        ]
    )

    id_producto = IntegerField(
        "ID del producto",
        validators=[
            DataRequired(
                message="El ID del producto es obligatorio."
            ),
            NumberRange(
                min=1,
                message="El ID del producto debe ser mayor que 0."
            )
        ]
    )

    placa = StringField(
        "Placa",
        validators=[
            Length(
                min=7,
                max=8,
                message="La placa debe tener entre 7 y 8 caracteres."
            )
        ]
    )

    servicio = StringField(
        "Servicio",
        validators=[
            Length(
                min=3,
                max=100,
                message="El servicio debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    horas = IntegerField(
        "Horas",
        validators=[
            DataRequired(
                message="Las horas son obligatorias."
            ),
            NumberRange(
                min=1,
                message="Las horas deben ser mayores a 0."
            )
        ]
    )

    total = FloatField(
        "Total",
    )

    submit = SubmitField("Guardar factura")