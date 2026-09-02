from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError


def validar_precio(form, field):

    if not field.data or not field.data.strip():
        raise ValidationError("El precio es obligatorio.")

    try:
        precio = float(field.data)
    except ValueError:
        raise ValidationError("El precio debe ser un número válido.")

    if precio <= 0:
        raise ValidationError("El precio debe ser mayor que 0.")


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del servicio",
        validators=[
            DataRequired(message="El nombre del servicio es obligatorio."),
            Length(
                min=3,
                max=50,
                message="El nombre debe tener entre 3 y 50 caracteres."
            )
        ]
    )

    descripcion = StringField(
        "Descripción",
        validators=[
            DataRequired(message="La descripción es obligatoria."),
            Length(
                min=5,
                max=150,
                message="La descripción debe tener entre 5 y 150 caracteres."
            )
        ]
    )

    precio = StringField(
        "Precio",
        validators=[
            validar_precio
        ]
    )

    disponible = BooleanField(
        "Disponible"
    )

    submit = SubmitField("Guardar servicio")