document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       SISTEMA DE REGISTRO DE VEHÍCULOS
       Bootstrap + Validaciones + LocalStorage
       Preparado para futura integración con Flask
    ====================================================== */

    /* ==========================
       REFERENCIAS DEL DOM
    ========================== */

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

    /* ==========================
       NUEVOS ELEMENTOS BOOTSTRAP
    ========================== */

    const spinner =
        document.getElementById("spinnerCarga");

    const detalleModal =
        document.getElementById("detalleModal");

    const modalBootstrap =
        new bootstrap.Modal(
            document.getElementById("modalRegistro")
        );

    /* ==========================
       LOCAL STORAGE
    ========================== */

    let registros =
        JSON.parse(
            localStorage.getItem("registros")
        ) || [];

    /* =====================================================
                    VALIDACIONES
    ====================================================== */

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

        mostrarCorrecto(
            nombre,
            errorNombre
        );

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

    /* =====================================================
                ESTADOS VISUALES
    ====================================================== */

    function mostrarError(
        input,
        contenedor,
        texto
    ) {

        input.classList.remove("is-valid");

        input.classList.add("is-invalid");

        contenedor.textContent = texto;

    }

    function mostrarCorrecto(
        input,
        contenedor
    ) {

        input.classList.remove("is-invalid");

        input.classList.add("is-valid");

        contenedor.textContent = "";

    }

    /* =====================================================
          VALIDACIÓN EN TIEMPO REAL
    ====================================================== */

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

    /* =====================================================
             ENVÍO DEL FORMULARIO
    ====================================================== */

    formulario.addEventListener(
        "submit",
        function (evento) {

            evento.preventDefault();

            const nombreValido =
                validarNombre();

            const placaValida =
                validarDescripcion();

            const categoriaValida =
                validarCategoria();

            if (
                !nombreValido ||
                !placaValida ||
                !categoriaValida
            ) {

                mensaje.innerHTML = `
                    <div class="alert alert-danger">
                        Corrija los errores antes de registrar el vehículo.
                    </div>
                `;

                return;

            }

            /* ======================================
               MOSTRAR SPINNER
            ======================================= */

            spinner.classList.remove("d-none");

            /* ======================================
               SIMULACIÓN DE CARGA
            ======================================= */

            setTimeout(function () {

                spinner.classList.add("d-none");

                const nuevoRegistro = {

                    id: Date.now(),

                    nombre:
                        nombre.value.trim(),

                    descripcion:
                        descripcion.value.trim(),

                    categoria:
                        categoria.value

                };

                registros.push(
                    nuevoRegistro
                );

                localStorage.setItem(
                    "registros",
                    JSON.stringify(registros)
                );

                renderizarRegistros();

                mensaje.innerHTML = `
                    <div class="alert alert-success alert-dismissible fade show">

                        Vehículo registrado correctamente.

                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="alert">
                        </button>

                    </div>
                `;

                detalleModal.innerHTML = `

                    <p>

                        <strong>Propietario:</strong>

                        ${nuevoRegistro.nombre}

                    </p>

                    <p>

                        <strong>Placa:</strong>

                        ${nuevoRegistro.descripcion}

                    </p>

                    <p>

                        <strong>Tipo:</strong>

                        ${nuevoRegistro.categoria}

                    </p>

                `;

                modalBootstrap.show();

                formulario.reset();

                nombre.classList.remove("is-valid");
                descripcion.classList.remove("is-valid");
                categoria.classList.remove("is-valid");

                errorNombre.textContent = "";
                errorDescripcion.textContent = "";
                errorCategoria.textContent = "";

            }, 1500);

        }

    );

    /* =====================================================
            RENDERIZAR REGISTROS
    ====================================================== */
        function renderizarRegistros() {

        /* ===========================================
           LIMPIAR CONTENEDOR
        ============================================ */

        listaRegistros.innerHTML = "";

        /* ===========================================
           SI NO EXISTEN REGISTROS
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
           RECORRER REGISTROS
        ============================================ */

        registros.forEach(function (registro) {

            const tarjeta =
                document.createElement("div");

            tarjeta.className =
                "card mb-3 shadow-sm";

            tarjeta.innerHTML = `

                <div class="card-body">

                    <div class="d-flex justify-content-between align-items-start">

                        <div>

                            <h5 class="card-title">

                                ${registro.nombre}

                            </h5>

                            <p class="card-text mb-2">

                                <strong>Placa:</strong>

                                ${registro.descripcion}

                            </p>

                            <span class="badge bg-primary">

                                ${registro.categoria}

                            </span>

                        </div>

                        <button
                            class="btn btn-danger btn-sm">

                            Eliminar

                        </button>

                    </div>

                </div>

            `;

            /* ===========================================
               BOTÓN ELIMINAR
            ============================================ */

            const botonEliminar =
                tarjeta.querySelector("button");

            botonEliminar.addEventListener(
                "click",
                function () {

                    if (
                        confirm(
                            "¿Está seguro de eliminar este registro?"
                        )
                    ) {

                        registros = registros.filter(
                            function (vehiculo) {

                                return (
                                    vehiculo.id !== registro.id
                                );

                            }
                        );

                        localStorage.setItem(
                            "registros",
                            JSON.stringify(registros)
                        );

                        renderizarRegistros();

                        mensaje.innerHTML = `

                            <div class="alert alert-warning alert-dismissible fade show">

                                Registro eliminado correctamente.

                                <button
                                    type="button"
                                    class="btn-close"
                                    data-bs-dismiss="alert">

                                </button>

                            </div>

                        `;

                    }

                }

            );

            listaRegistros.appendChild(
                tarjeta
            );

        });

        /* ===========================================
           ACTUALIZAR CONTADOR
        ============================================ */

        totalRegistros.textContent =
            registros.length;

    }

    /* ===========================================
       CARGAR REGISTROS AL INICIAR
    ============================================ */

    renderizarRegistros();

});