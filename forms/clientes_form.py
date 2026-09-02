from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ClienteForm(FlaskForm):

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(min=3, max=50, message="El nombre debe tener entre 3 y 50 caracteres.")
        ]
    )

    cedula = StringField(
        "Cédula",
        validators=[
            DataRequired(message="La cédula es obligatoria."),
            Length(min=10, max=10, message="La cédula debe tener 10 dígitos.")
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(min=10, max=10, message="El teléfono debe tener 10 dígitos.")
        ]
    )

    placa = StringField(
        "Placa",
        validators=[
            DataRequired(message="La placa es obligatoria."),
            Length(min=8, max=8, message="La placa debe tener 8 caracteres.")
        ]
    )

    submit = SubmitField("Guardar Cliente")