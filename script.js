document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       SISTEMA DE REGISTRO DE VEHÍCULOS
       Archivo para futura integración con Flask.
       El contenido dinámico será posteriormente reemplazado
       por plantillas Jinja (Flask).
    ====================================================== */

    /* -------------------------
       REFERENCIAS DEL DOM
    -------------------------- */

    const formulario = document.getElementById("formulario");

    const nombre = document.getElementById("nombre");
    const descripcion = document.getElementById("descripcion");
    const categoria = document.getElementById("categoria");

    const listaRegistros = document.getElementById("listaRegistros");
    const totalRegistros = document.getElementById("total");
    const mensaje = document.getElementById("mensaje");

    const errorNombre = document.getElementById("errorNombre");
    const errorDescripcion = document.getElementById("errorDescripcion");
    const errorCategoria = document.getElementById("errorCategoria");

    /* ------------------------
       ARREGLO DE OBJETOS
       (Contenido dinámico)
    --------------------------- */

    let registros =
        JSON.parse(localStorage.getItem("registros")) || [];

    /* ===========================
       FUNCIONES DE VALIDACIÓN
    =========================== */

    function validarNombre() {

        const valor = nombre.value.trim();

        if (valor === "") {

            mostrarError(
                nombre,
                errorNombre,
                "El nombre es obligatorio."
            );

            return false;

        }

        if (valor.length < 5) {

            mostrarError(
                nombre,
                errorNombre,
                "Debe contener mínimo 5 caracteres."
            );

            return false;

        }

        mostrarCorrecto(nombre, errorNombre);

        return true;

    }

    function validarDescripcion() {

        const valor = descripcion.value.trim();

        if (valor === "") {

            mostrarError(
                descripcion,
                errorDescripcion,
                "La placa es obligatoria."
            );

            return false;

        }

        if (valor.length < 6) {

            mostrarError(
                descripcion,
                errorDescripcion,
                "Debe contener al menos 6 caracteres."
            );

            return false;

        }

        mostrarCorrecto(
            descripcion,
            errorDescripcion
        );

        return true;

    }

    function validarCategoria() {

        if (categoria.value === "") {

            mostrarError(
                categoria,
                errorCategoria,
                "Seleccione el tipo de vehículo."
            );

            return false;

        }

        mostrarCorrecto(
            categoria,
            errorCategoria
        );

        return true;

    }

    /* -------------------------
       ESTADOS VISUALES
    ------------------------- */

    function mostrarError(
        input,
        contenedorError,
        texto
    ) {

        input.classList.remove("is-valid");
        input.classList.add("is-invalid");

        contenedorError.textContent = texto;

    }

    function mostrarCorrecto(
        input,
        contenedorError
    ) {

        input.classList.remove("is-invalid");
        input.classList.add("is-valid");

        contenedorError.textContent = "";

    }

    /* ------------------------
       VALIDACIÓN EN TIEMPO REAL
    --------------------------- */

    nombre.addEventListener(
        "input",
        validarNombre
    );

    nombre.addEventListener(
        "blur",
        validarNombre
    );

    descripcion.addEventListener(
        "input",
        validarDescripcion
    );

    descripcion.addEventListener(
        "blur",
        validarDescripcion
    );

    categoria.addEventListener(
        "change",
        validarCategoria
    );

    categoria.addEventListener(
        "blur",
        validarCategoria
    );

    /* ===========================
       SUBMIT DEL FORMULARIO
    =========================== */
        formulario.addEventListener("submit", function (evento) {

        evento.preventDefault();

        /* ===========================
           VALIDACIÓN FORMULARIO
        =========================== */

        const nombreValido = validarNombre();
        const placaValida = validarDescripcion();
        const categoriaValida = validarCategoria();

        if (!nombreValido || !placaValida || !categoriaValida) {

            mensaje.innerHTML = `
                <div class="alert alert-danger">
                    Corrija los errores antes de registrar el vehículo.
                </div>
            `;

            return;

        }

        /* ===========================
           OBJETO DEL VEHÍCULO
        =========================== */

        const nuevoRegistro = {

            id: Date.now(),

            nombre: nombre.value.trim(),

            descripcion: descripcion.value.trim(),

            categoria: categoria.value

        };

        /* ===========================
           AGREGAR AL ARREGLO
        =========================== */

        registros.push(nuevoRegistro);

        /* ===========================
           GUARDAR EN LOCALSTORAGE
        =========================== */

        localStorage.setItem(
            "registros",
            JSON.stringify(registros)
        );

        /* ===========================
           ACTUALIZAR CONTENIDO DINÁMICO
        =========================== */

        renderizarRegistros();

        /* ===========================
           MENSAJE DE ÉXITO
        =========================== */

        mensaje.innerHTML = `
            <div class="alert alert-success">
                Vehículo registrado correctamente.
            </div>
        `;

        /* ===========================
           LIMPIEZA DE FORMULARIO
        =========================== */

        formulario.reset();

        nombre.classList.remove("is-valid");
        descripcion.classList.remove("is-valid");
        categoria.classList.remove("is-valid");

        errorNombre.textContent = "";
        errorDescripcion.textContent = "";
        errorCategoria.textContent = "";

    });

    /* ===========================
       RENDERIZAR REGISTROS
    =========================== */
        function renderizarRegistros() {

        /* ===========================================
           LIMPIAR EL CONTENEDOR
        ============================================ */

        listaRegistros.innerHTML = "";

        /* ===========================================
           CONDICIÓN
           Mostrar mensaje cuando no existan registros
        ============================================ */

        if (registros.length === 0) {

            listaRegistros.innerHTML = `
                <div class="alert alert-warning text-center">
                    No existen vehículos registrados.
                </div>
            `;

            totalRegistros.textContent = "0";

            return;

        }

        /* ===========================================
           ESTRUCTURA REPETITIVA (forEach)
        ============================================ */

        registros.forEach(function (registro) {

            const tarjeta = document.createElement("div");

            tarjeta.className = "card mb-3 shadow-sm";

            tarjeta.innerHTML = `

                <div class="card-body">

                    <h5 class="card-title">
                        ${registro.nombre}
                    </h5>

                    <p class="card-text">

                        <strong>Placa:</strong>
                        ${registro.descripcion}

                    </p>

                    <p>

                        <span class="badge bg-primary">

                            ${registro.categoria}

                        </span>

                    </p>

                    <button
                        class="btn btn-danger btn-sm">

                        Eliminar

                    </button>

                </div>

            `;

            /* ===========================
               BOTÓN ELIMINAR
            =========================== */

            const botonEliminar =
                tarjeta.querySelector("button");

            botonEliminar.addEventListener(
                "click",
                function () {

                    registros = registros.filter(function (vehiculo) {

                        return vehiculo.id !== registro.id;

                    });

                    localStorage.setItem(
                        "registros",
                        JSON.stringify(registros)
                    );

                    renderizarRegistros();

                }
            );

            listaRegistros.appendChild(tarjeta);

        });

        /* ===========================
           ACTUALIZAR CONTADOR
        =========================== */

        totalRegistros.textContent = registros.length;

    }

    /* ===========================
       CARGAR INFORMACIÓN
       CARGAR REGISTROS AL INICIAR LA PÁGINA
    ============================================ */

    renderizarRegistros();


});