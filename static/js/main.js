

document.addEventListener("DOMContentLoaded", () => {

    /* ==============================
        MENÚ MÓVIL
       ============================== */

    const menuButton = document.querySelector("[data-menu-toggle]");
    const mobileMenu = document.querySelector("[data-mobile-menu]");

    if (menuButton && mobileMenu) {

        menuButton.addEventListener("click", () => {

            const menuAbierto = mobileMenu.classList.toggle(
                "menu-movil--abierto"
            );

            menuButton.setAttribute(
                "aria-expanded",
                menuAbierto ? "true" : "false"
            );

            menuButton.setAttribute(
                "aria-label",
                menuAbierto ? "Cerrar menú" : "Abrir menú"
            );
        });
    }


    /* ==============================
        CARRUSEL DE PROYECTOS
       ============================== */

    const carruseles = document.querySelectorAll("[data-carrusel]");

    carruseles.forEach((carrusel) => {

        const pista = carrusel.querySelector(".carrusel-pista");
        const botonAnterior = carrusel.querySelector(
            "[data-carrusel-anterior]"
        );
        const botonSiguiente = carrusel.querySelector(
            "[data-carrusel-siguiente]"
        );
        const indicador = carrusel.querySelector(
            "[data-carrusel-indicador]"
        );

        if (
            !pista ||
            !botonAnterior ||
            !botonSiguiente ||
            !indicador
        ) {
            return;
        }


        /* ------------------------------
            Obtener tarjetas
           ------------------------------ */

        const tarjetas = Array.from(
            pista.children
        ).filter((elemento) =>
            elemento.classList.contains("tarjeta-proyecto")
        );


        if (tarjetas.length === 0) {
            return;
        }


        /* ------------------------------
            Crear páginas de 5 tarjetas
           ------------------------------ */

        const cantidadPorPagina = 5;
        const paginas = [];

        for (
            let inicio = 0;
            inicio < tarjetas.length;
            inicio += cantidadPorPagina
        ) {

            const pagina = document.createElement("div");

            pagina.classList.add("carrusel-pagina");

            const tarjetasPagina = tarjetas.slice(
                inicio,
                inicio + cantidadPorPagina
            );

            tarjetasPagina.forEach((tarjeta) => {
                pagina.appendChild(tarjeta);
            });

            paginas.push(pagina);
            pista.appendChild(pagina);
        }


        /* ------------------------------
            Estado inicial
           ------------------------------ */

        let paginaActual = 0;

        const cantidadPaginas = paginas.length;


        /* ------------------------------
            Actualizar carrusel
           ------------------------------ */

        function actualizarCarrusel() {

            const desplazamiento = paginaActual * 100;

            pista.style.transform =
                `translateX(-${desplazamiento}%)`;


            indicador.textContent =
                `${paginaActual + 1} / ${cantidadPaginas}`;


            botonAnterior.disabled =
                paginaActual === 0;


            botonSiguiente.disabled =
                paginaActual === cantidadPaginas - 1;
        }


        /* ------------------------------
            Navegación anterior
           ------------------------------ */

        botonAnterior.addEventListener("click", () => {

            if (paginaActual === 0) {
                return;
            }

            paginaActual -= 1;

            actualizarCarrusel();
        });


        /* ------------------------------
            Navegación siguiente
           ------------------------------ */

        botonSiguiente.addEventListener("click", () => {

            if (paginaActual >= cantidadPaginas - 1) {
                return;
            }

            paginaActual += 1;

            actualizarCarrusel();
        });


        /* ------------------------------
            Estado inicial
           ------------------------------ */

        actualizarCarrusel();
    });

});