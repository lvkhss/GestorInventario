document.addEventListener("DOMContentLoaded", () => {
    // 1. Buscar el input real del filtro (sin ID, pero está dentro de .buscador)
    const filtro = document.querySelector(".buscador input");

    // 2. Seleccionar las filas de productos
    const filas = document.querySelectorAll(".proveedor-fila");

    // 3. Filtrar productos
    filtro.addEventListener("input", () => {
        const valor = filtro.value.toLowerCase();
        filas.forEach(fila => {
            const texto = fila.textContent.toLowerCase();
            fila.style.display = texto.includes(valor) ? "grid" : "none";
        });
    });

    // 4. Delegación de eventos para editar/eliminar
    document.body.addEventListener("click", (e) => {
        // Eliminar producto
        if (e.target.classList.contains("proveedor-delete-btn")) {
            const fila = e.target.closest(".proveedor-fila");
            const nombre = fila.children[0].textContent;
            if (confirm(`¿Eliminar el producto "${nombre}"?`)) {
                fila.remove();
            }
        }

        // Editar producto
        if (e.target.classList.contains("proveedor-edit-btn")) {
            const fila = e.target.closest(".proveedor-fila");
            const nombre = fila.children[0].textContent;
            alert(`Editar producto: ${nombre}`);
        }
    });
});

//MODAL INV
// Obtener el modal y el botón de agregar
const modal = document.getElementById("modalAgregar");
const btnAgregar = document.getElementById("btnAgregar");
const spanCerrar = document.querySelector(".close-btn");

// Abrir el modal cuando el usuario hace clic en el botón de agregar
btnAgregar.onclick = function() {
  modal.style.display = "block";
}

// Cerrar el modal cuando el usuario hace clic en la "X"
spanCerrar.onclick = function() {
  modal.style.display = "none";
}

// Cerrar el modal si el usuario hace clic fuera de la modal
window.onclick = function(event) {
  if (event.target === modal) {
    modal.style.display = "none";
  }
}
