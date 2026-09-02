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

    cliente = StringField(
        "Cliente",
        validators=[
            DataRequired(
                message="El cliente es obligatorio."
            ),
            Length(
                min=3,
                max=50,
                message="El nombre del cliente debe tener entre 3 y 50 caracteres."
            )
        ]
    )

    placa = StringField(
        "Placa",
        validators=[
            DataRequired(
                message="La placa es obligatoria."
            ),
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
            DataRequired(
                message="El servicio es obligatorio."
            ),
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
        validators=[
            DataRequired(
                message="El total es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El total no puede ser negativo."
            )
        ]
    )

    submit = SubmitField("Guardar factura")