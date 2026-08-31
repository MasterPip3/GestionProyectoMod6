



document.addEventListener("DOMContentLoaded", () => {
    const menuButton = document.querySelector("[data-menu-toggle]");
    const mobileMenu = document.querySelector("[data-mobile-menu]");

    if (!menuButton || !mobileMenu) {
        return;
    }

    menuButton.addEventListener("click", () => {
        const menuAbierto = mobileMenu.classList.toggle("menu-movil-abierto");

        menuButton.setAttribute(
            "aria-expanded",
            menuAbierto ? "true" : "false"
        );
    });
});