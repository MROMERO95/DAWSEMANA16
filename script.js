document.addEventListener("DOMContentLoaded", function () {

const form = document.getElementById("formulario");

const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const lista = document.getElementById("listaRegistros");
const total = document.getElementById("total");
const mensaje = document.getElementById("mensaje");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

let registros = JSON.parse(localStorage.getItem("registros")) || [];

/* =========================
   FUNCIONES DE VALIDACIÓN
========================= */

function validarNombre() {

    const valor = nombre.value.trim();

    if (valor === "") {
        setError(nombre, errorNombre, "El nombre es obligatorio");
        return false;
    }

    if (valor.length < 5) {
        setError(nombre, errorNombre, "Mínimo 5 caracteres");
        return false;
    }

    setSuccess(nombre, errorNombre);
    return true;
}

function validarDescripcion() {

    const valor = descripcion.value.trim();

    if (valor === "") {
        setError(descripcion, errorDescripcion, "La placa es obligatoria");
        return false;
    }

    if (valor.length < 6) {
        setError(descripcion, errorDescripcion, "Debe tener al menos 6 caracteres");
        return false;
    }

    setSuccess(descripcion, errorDescripcion);
    return true;
}

function validarCategoria() {

    if (categoria.value === "") {
        setError(categoria, errorCategoria, "Seleccione una categoría");
        return false;
    }

    setSuccess(categoria, errorCategoria);
    return true;
}

/* =========================
   ESTADOS VISUALES
========================= */

function setError(input, errorDiv, mensajeError) {
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    errorDiv.textContent = mensajeError;
}

function setSuccess(input, errorDiv) {
    input.classList.add("is-valid");
    input.classList.remove("is-invalid");
    errorDiv.textContent = "";
}

/* =========================
   VALIDACIÓN EN TIEMPO REAL
========================= */

nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

categoria.addEventListener("change", validarCategoria);
categoria.addEventListener("blur", validarCategoria);

/* =========================
   SUBMIT DEL FORMULARIO
========================= */

form.addEventListener("submit", function (e) {

    e.preventDefault();

    const n1 = validarNombre();
    const n2 = validarDescripcion();
    const n3 = validarCategoria();

    if (!n1 || !n2 || !n3) {

        mensaje.innerHTML = `
        <div class="alert alert-danger">
            Corrige los errores antes de registrar
        </div>`;

        return;
    }

    const registro = {
        id: Date.now(),
        nombre: nombre.value.trim(),
        descripcion: descripcion.value.trim(),
        categoria: categoria.value
    };

    registros.push(registro);
    localStorage.setItem("registros", JSON.stringify(registros));

    renderizar();

    mensaje.innerHTML = `
    <div class="alert alert-success">
        Vehículo registrado correctamente
    </div>`;

    form.reset();

    nombre.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");

});

/* =========================
   RENDERIZAR REGISTROS
========================= */

function renderizar() {

    lista.innerHTML = "";

    registros.forEach(reg => {

        const card = document.createElement("div");
        card.classList.add("card", "p-2", "mb-2");

        const body = document.createElement("div");
        body.classList.add("card-body");

        const titulo = document.createElement("h5");
        titulo.textContent = reg.nombre;

        const placa = document.createElement("p");
        placa.textContent = "Placa: " + reg.descripcion;

        const tipo = document.createElement("span");
        tipo.classList.add("badge", "bg-primary");
        tipo.textContent = reg.categoria;

        const btn = document.createElement("button");
        btn.textContent = "Eliminar";
        btn.classList.add("btn", "btn-danger", "btn-sm", "mt-2");

        btn.addEventListener("click", function () {

            registros = registros.filter(r => r.id !== reg.id);
            localStorage.setItem("registros", JSON.stringify(registros));

            renderizar();
        });

        body.appendChild(titulo);
        body.appendChild(placa);
        body.appendChild(tipo);
        body.appendChild(document.createElement("br"));
        body.appendChild(btn);

        card.appendChild(body);
        lista.appendChild(card);

    });

    total.textContent = registros.length;
}

/* cargar datos al inicio */
renderizar();

});