


/* menu-hamburguesa */
document.addEventListener("DOMContentLoaded", () => {
    const menuButton = document.querySelector("[data-menu-toggle]");
    const mobileMenu = document.querySelector("[data-mobile-menu]");

    if (!menuButton || !mobileMenu) {
        return;
    }

    menuButton.addEventListener("click", () => {
        const menuAbierto = mobileMenu.classList.toggle("menu-movil--abierto");

        menuButton.setAttribute(
            "aria-expanded",
            menuAbierto ? "true" : "false"
        );
    });
});


/* Carrusel */
document.addEventListener("DOMContentLoaded", () => {

    const visores = document.querySelectorAll("[data-visor]");

    visores.forEach((visor) => {

        const pistas = visor.querySelector("[data-visor-pistas]");
        const botonAnterior = visor.querySelector("[data-visor-anterior]");
        const botonSiguiente = visor.querySelector("[data-visor-siguiente]");

        if (!pistas || !botonAnterior || !botonSiguiente) {
            return;
        }

        const tarjetas = Array.from(
            pistas.querySelectorAll(".tarjeta-proyecto")
        );

        const cantidadPorPagina = 5;
        const paginas = [];

        tarjetas.forEach((tarjeta, indice) => {

            const indicePagina = Math.floor(
                indice / cantidadPorPagina
            );

            if (!paginas[indicePagina]) {

                const pagina = document.createElement("div");

                pagina.classList.add("visor-pagina");

                paginas.push(pagina);
                pistas.appendChild(pagina);
            }

            paginas[indicePagina].appendChild(tarjeta);

        });

        let paginaActual = 0;

        const actualizarVisor = () => {

            pistas.style.transform =
                `translateX(-${paginaActual * 100}%)`;

            botonAnterior.disabled =
                paginaActual === 0;

            botonSiguiente.disabled =
                paginaActual === paginas.length - 1;

        };

        botonAnterior.addEventListener("click", () => {

            if (paginaActual > 0) {
                paginaActual -= 1;
                actualizarVisor();
            }

        });

        botonSiguiente.addEventListener("click", () => {

            if (paginaActual < paginas.length - 1) {
                paginaActual += 1;
                actualizarVisor();
            }

        });

        actualizarVisor();

    });

});