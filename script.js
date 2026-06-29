document.addEventListener("DOMContentLoaded", function () {

const form = document.getElementById("formulario");
const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const lista = document.getElementById("listaRegistros");
const total = document.getElementById("total");
const mensaje = document.getElementById("mensaje");

let registros = JSON.parse(localStorage.getItem("registros")) || [];

let contador = registros.length;

// cargar al inicio
renderizar();

form.addEventListener("submit", function (e) {
e.preventDefault();

// validación
if (nombre.value.trim() === "" ||
descripcion.value.trim() === "" ||
categoria.value === "") {

mensaje.innerHTML = `
<div class="alert alert-danger">
Todos los campos son obligatorios
</div>`;
return;
}

mensaje.innerHTML = "";

// nuevo registro
const registro = {
id: Date.now(),
nombre: nombre.value,
descripcion: descripcion.value,
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

});

// renderizar registros
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

// botón eliminar
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

});