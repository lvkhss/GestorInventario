// ===================================
// TABLAS - Toggle columnas alternadas (FUNCIÓN GLOBAL)
// ===================================
let toggleButton, table, stripedColumns;
const inactiveSVG = `<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="none" viewBox="0 0 24 24"><path stroke="currentColor" stroke-linecap="round" stroke-width="2" d="M12.0001 20v-4M7.00012 4h9.99998M9.00012 5v5c0 .5523-.46939 1.0045-.94861 1.279-1.43433.8217-2.60135 3.245-2.25635 4.3653.07806.2535.35396.3557.61917.3557H17.5859c.2652 0 .5411-.1022.6192-.3557.3449-1.1204-.8221-3.5436-2.2564-4.3653-.4792-.2745-.9486-.7267-.9486-1.279V5c0-.55228-.4477-1-1-1h-4c-.55226 0-.99998.44772-.99998 1Z"/></svg>`;
const activeSVG = `<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v4.997a.31.31 0 0 1-.068.113c-.08.098-.213.207-.378.301-.947.543-1.713 1.54-2.191 2.488A6.237 6.237 0 0 0 4.82 14.4c-.1.48-.138 1.031.018 1.539C5.12 16.846 6.02 17 6.414 17H11v3a1 1 0 1 0 2 0v-3h4.586c.395 0 1.295-.154 1.575-1.061.156-.508.118-1.059.017-1.539a6.241 6.241 0 0 0-.541-1.5c-.479-.95-1.244-1.946-2.191-2.489a1.393 1.393 0 0 1-.378-.301.309.309 0 0 1-.068-.113V5h1a1 1 0 1 0 0-2H7a1 1 0 1 0 0 2h1Z"/></svg>`;

function initializeToggleButton() {
    toggleButton = document.querySelector('.dynamic-table-button') || document.querySelector('#toggleColumns');
    table = document.querySelector('.table');

    if (toggleButton && table) {
        // Recuperar estado desde localStorage
        stripedColumns = localStorage.getItem('stripedColumns') === 'true';

        // Aplicar estado inicial
        updateToggleState();

        // Remover listeners anteriores y agregar nuevo
        toggleButton.replaceWith(toggleButton.cloneNode(true));
        toggleButton = document.querySelector('.dynamic-table-button') || document.querySelector('#toggleColumns');
        
        toggleButton.addEventListener('click', function (e) {
            e.preventDefault();
            stripedColumns = !stripedColumns;
            updateToggleState();
        });
    }
}

function updateToggleState() {
    if (stripedColumns) {
        table.classList.add('striped-columns');
        toggleButton.innerHTML = activeSVG;
        toggleButton.classList.add('active');
    } else {
        table.classList.remove('striped-columns');
        toggleButton.innerHTML = inactiveSVG;
        toggleButton.classList.remove('active');
    }
    localStorage.setItem('stripedColumns', stripedColumns);
}

function reapplyToggleState() {
    const savedState = localStorage.getItem('stripedColumns') === 'true';
    const currentTable = document.querySelector('.table');
    if (currentTable && savedState) {
        currentTable.classList.add('striped-columns');
    }
}

// Inicializar al cargar la página
document.addEventListener('DOMContentLoaded', initializeToggleButton);

// ===================================
// INVENTARIO - Actualización de tabla
// ===================================
function updateTable() {
    const query = document.getElementById("searchInput").value;
    const type = document.getElementById("filterType").value;

    let url = `/inventario/?`;
    if (query) url += `q=${encodeURIComponent(query)}&`;
    if (type) url += `type=${encodeURIComponent(type)}`;

    fetch(url)
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const htmlDoc = parser.parseFromString(data, "text/html");
            const newContent = htmlDoc.querySelector("#tablaProductos").innerHTML;
            document.getElementById("tablaProductos").innerHTML = newContent;
            
            // RE-INICIALIZAR el botón toggle
            initializeToggleButton();
        });
}

// ===================================
// HISTORIAL - Actualización de tabla
// ===================================
function updateHistorialTable() {
    const query = document.getElementById("searchInput").value;
    const type = document.getElementById("filterType").value;
    const userElement = document.getElementById("filterUser");
    const user = userElement ? userElement.value : "";
    const startDateInput = document.getElementById("startDate");
    const endDateInput = document.getElementById("endDate");
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;

    if (startDate && endDate && new Date(startDate) > new Date(endDate)) {
        alert("La fecha de inicio no puede ser posterior a la fecha de fin.");
        endDateInput.value = "";

        fetch('/historial/')
            .then(response => response.text())
            .then(data => {
                const parser = new DOMParser();
                const htmlDoc = parser.parseFromString(data, "text/html");
                const newContent = htmlDoc.querySelector("#tablaHistorial").innerHTML;
                document.getElementById("tablaHistorial").innerHTML = newContent;
                
                // RE-INICIALIZAR el botón toggle
                initializeToggleButton();
            });
        return;
    }

    let url = '/historial/?';
    if (query) url += `q=${encodeURIComponent(query)}&`;
    if (type) url += `type=${encodeURIComponent(type)}&`;
    if (user) url += `user=${encodeURIComponent(user)}&`;
    if (startDate) url += `start=${encodeURIComponent(startDate)}&`;
    if (endDate) url += `end=${encodeURIComponent(endDate)}`;

    fetch(url)
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const htmlDoc = parser.parseFromString(data, "text/html");
            const newContent = htmlDoc.querySelector("#tablaHistorial").innerHTML;
            document.getElementById("tablaHistorial").innerHTML = newContent;
            
            // RE-INICIALIZAR el botón toggle
            initializeToggleButton();
        });
}

// ===================================
// USER MOVEMENTS - Actualización de tabla
// ===================================
function updateUserMovementsTable() {
    const query = document.getElementById("searchInput").value;
    const type = document.getElementById("filterType").value;
    const startDateInput = document.getElementById("startDate");
    const endDateInput = document.getElementById("endDate");
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;

    if (startDate && endDate && new Date(startDate) > new Date(endDate)) {
        alert("La fecha de inicio no puede ser posterior a la fecha de fin.");
        endDateInput.value = "";

        fetch('/user-mov/')
            .then(response => response.text())
            .then(data => {
                const parser = new DOMParser();
                const htmlDoc = parser.parseFromString(data, "text/html");
                const newContent = htmlDoc.querySelector("#tablaHistorial").innerHTML;
                document.getElementById("tablaHistorial").innerHTML = newContent;
                
                // RE-INICIALIZAR el botón toggle
                initializeToggleButton();
            });
        return;
    }

    let url = '/user-mov/?';
    if (query) url += `q=${encodeURIComponent(query)}&`;
    if (type) url += `type=${encodeURIComponent(type)}&`;
    if (startDate) url += `start=${encodeURIComponent(startDate)}&`;
    if (endDate) url += `end=${encodeURIComponent(endDate)}`;

    fetch(url)
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const htmlDoc = parser.parseFromString(data, "text/html");
            const newContent = htmlDoc.querySelector("#tablaHistorial").innerHTML;
            document.getElementById("tablaHistorial").innerHTML = newContent;
            
            // RE-INICIALIZAR el botón toggle
            initializeToggleButton();
        });
}

// Detectar si estamos en la página de movimientos del usuario
document.addEventListener('DOMContentLoaded', function () {
    // Verificar si estamos en la página de user-movimientos (soporta /user-mov/ y /user-mov)
    if (window.location.pathname.startsWith('/user-mov')) {
        const searchInput = document.getElementById("searchInput");
        const filterType = document.getElementById("filterType");
        const startDate = document.getElementById("startDate");
        const endDate = document.getElementById("endDate");

        if (searchInput) {
            searchInput.addEventListener("input", updateUserMovementsTable);
        }

        if (filterType) {
            filterType.addEventListener("change", updateUserMovementsTable);
        }

        if (startDate) {
            startDate.addEventListener("change", updateUserMovementsTable);
        }

        if (endDate) {
            endDate.addEventListener("change", updateUserMovementsTable);
        }
    }
});

// ===================================
// INVENTARIO - Event listeners
// ===================================
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById("searchInput");
    const filterType = document.getElementById("filterType");

    if (searchInput) {
        searchInput.addEventListener("input", updateTable);
    }

    if (filterType) {
        filterType.addEventListener("change", updateTable);
    }
});

// ===================================
// HISTORIAL - Event listeners
// ===================================
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById("searchInput");
    const filterType = document.getElementById("filterType");
    const filterUser = document.getElementById("filterUser");
    const startDate = document.getElementById("startDate");
    const endDate = document.getElementById("endDate");

    // Solo agregar listeners si estamos en la página de historial
    if (window.location.pathname.includes('/historial/')) {
        if (searchInput) {
            searchInput.addEventListener("input", updateHistorialTable);
        }

        if (filterType) {
            filterType.addEventListener("change", updateHistorialTable);
        }

        if (filterUser) {
            filterUser.addEventListener("change", updateHistorialTable);
        }

        if (startDate) {
            startDate.addEventListener("change", updateHistorialTable);
        }

        if (endDate) {
            endDate.addEventListener("change", updateHistorialTable);
        }
    }
});

// ===================================
// INVENTARIO - Confirmación de eliminación
// ===================================
function confirmDelete(productId, productName) {
    if (confirm(`¿Está seguro que desea eliminar el producto "${productName}"?\n\nEsta acción no se puede deshacer.`)) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/productos/${productId}/delete/`;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        form.appendChild(csrfInput);

        document.body.appendChild(form);
        form.submit();
    }
}

// ===================================
// EDIT_ITEM - Manejo de motivos
// ===================================
document.addEventListener('DOMContentLoaded', function () {
    const motivoSelect = document.getElementById('id_motivo');
    const motivoExtra = document.getElementById('motivo_extra');
    const motivoHidden = document.getElementById('motivo_hidden');
    const form = document.querySelector('form');

    if (motivoSelect && motivoExtra && motivoHidden && form) {
        motivoSelect.addEventListener('change', function () {
            if (motivoSelect.value === "Otro") {
                motivoExtra.style.display = 'block';
                motivoExtra.disabled = false;
                motivoExtra.required = true;
                motivoExtra.focus();
            } else {
                motivoExtra.style.display = 'none';
                motivoExtra.disabled = true;
                motivoExtra.required = false;
                motivoExtra.value = "";
            }
        });

        form.addEventListener('submit', function (e) {
            if (motivoSelect.value === "") {
                e.preventDefault();
                alert('Por favor seleccione un motivo para el cambio.');
                return false;
            }

            if (motivoSelect.value === "Otro") {
                if (motivoExtra.value.trim() === "") {
                    e.preventDefault();
                    alert('Por favor especifique el motivo.');
                    motivoExtra.focus();
                    return false;
                }
                motivoHidden.value = motivoExtra.value.trim();
            } else {
                motivoHidden.value = motivoSelect.value;
            }
        });
    }
});

// ===================================
// SUPPLIERS_FORM - Formateo de RUT
// ===================================
document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('id_rut');

    if (rutInput) {
        rutInput.addEventListener('input', function () {
            let value = this.value.replace(/[^0-9kK]/g, ''); // Solo números y K

            if (value.length > 1) {
                // Separar cuerpo y dígito verificador
                let cuerpo = value.slice(0, -1);
                let dv = value.slice(-1).toUpperCase();

                // Formatear con guión
                this.value = cuerpo + '-' + dv;
            } else {
                this.value = value;
            }
        });

        // Validación adicional para RUT chileno
        rutInput.addEventListener('blur', function () {
            const rutValue = this.value;
            if (rutValue && !validateRUT(rutValue)) {
                this.style.borderColor = '#dc3545';
                // Mostrar mensaje de error si no existe
                let errorMsg = this.parentNode.querySelector('.rut-error');
                if (!errorMsg) {
                    errorMsg = document.createElement('small');
                    errorMsg.className = 'text-danger rut-error';
                    errorMsg.textContent = 'RUT inválido';
                    this.parentNode.appendChild(errorMsg);
                }
            } else {
                this.style.borderColor = '';
                // Remover mensaje de error si existe
                const errorMsg = this.parentNode.querySelector('.rut-error');
                if (errorMsg) {
                    errorMsg.remove();
                }
            }
        });
    }
});

// ===================================
// SUPPLIERS_FORM - Validación de RUT
// ===================================
function validateRUT(rut) {
    // Eliminar puntos y guión
    const cleanRUT = rut.replace(/[.-]/g, '');

    // Verificar formato básico (mínimo 8 caracteres, máximo 9)
    if (cleanRUT.length < 8 || cleanRUT.length > 9) {
        return false;
    }

    // Separar cuerpo y dígito verificador
    const cuerpo = cleanRUT.slice(0, -1);
    const dv = cleanRUT.slice(-1).toLowerCase();

    // Verificar que el cuerpo sean solo números
    if (!/^\d+$/.test(cuerpo)) {
        return false;
    }

    // Calcular dígito verificador
    let suma = 0;
    let multiplicador = 2;

    for (let i = cuerpo.length - 1; i >= 0; i--) {
        suma += parseInt(cuerpo[i]) * multiplicador;
        multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
    }

    const resto = suma % 11;
    const dvCalculado = resto === 0 ? '0' : resto === 1 ? 'k' : (11 - resto).toString();

    return dv === dvCalculado;
}

// ===================================
// REGISTER - Generar contraseña
// ===================================
function enablePassword() {
    const passwordField = document.getElementById('id_password');
    const confirmField = document.getElementById('id_confirm_password');

    // Generar contraseña automáticamente
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
    let password = '';
    for (let i = 0; i < 12; i++) {
        password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    passwordField.value = password;
    confirmField.value = password; // Auto llenar confirmación
}

// ===================================
// REGISTER - Copiar contraseña
// ===================================
function copyPassword() {
    const passwordField = document.getElementById('id_password');
    if (passwordField.value) {
        // Copiar usando Clipboard API si está disponible
        if (navigator.clipboard) {
            navigator.clipboard.writeText(passwordField.value).then(function() {
                // Mostrar toast flotante
                const toast = document.querySelector('.registro-toast.copy');
                if (toast) {
                    toast.style.display = 'block';
                    setTimeout(() => {
                        toast.style.display = 'none';
                    }, 2000);
                }
            });
        } else {
            // Fallback para navegadores antiguos
            passwordField.select();
            document.execCommand('copy');
            const toast = document.querySelector('.registro-toast.copy');
            if (toast) {
                toast.style.display = 'block';
                setTimeout(() => {
                    toast.style.display = 'none';
                }, 2000);
            }
        }
    }
}

// ===================================
// REGISTER - Toggle visibilidad contraseña
// ===================================
function togglePasswordVisibility() {
    const passwordField = document.getElementById('id_password');
    const toggleBtn = document.getElementById('togglePassword');

    if (passwordField && toggleBtn) {
        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            toggleBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-slash" viewBox="0 0 16 16">
                <path d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7 7 0 0 0-2.79.588l.77.771A6 6 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755q-.247.248-.517.486z"/>
                <path d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829"/>
                <path d="M3.35 5.47q-.27.24-.518.487A13 13 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7 7 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12z"/>
            </svg>`;
            toggleBtn.title = 'Ocultar contraseña';
        } else {
            passwordField.type = 'password';
            toggleBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye" viewBox="0 0 16 16">
                <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8M1.173 8a13 13 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5s3.879 1.168 5.168 2.457A13 13 0 0 1 14.828 8q-.086.13-.195.288c-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5s-3.879-1.168-5.168-2.457A13 13 0 0 1 1.172 8z"/>
                <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5M4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0"/>
            </svg>`;
            toggleBtn.title = 'Mostrar contraseña';
        }
    }
}

// ===================================
// REGISTER - Validación de formulario
// ===================================
document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.querySelector('form[method="POST"]');

    if (registerForm && document.getElementById('id_username')) {
        registerForm.addEventListener('submit', function (e) {
            const username = document.getElementById('id_username').value;
            const email = document.getElementById('id_email').value;
            const password1 = document.getElementById('id_password1').value;
            const password2 = document.getElementById('id_password2').value;

            // Verificar que todos los campos estén llenos
            if (!username || !email || !password1 || !password2) {
                e.preventDefault();
                alert('Por favor complete todos los campos');
                return false;
            }

            // Verificar que las contraseñas coincidan
            if (password1 !== password2) {
                e.preventDefault();
                alert('Las contraseñas no coinciden');
                return false;
            }
        });
    }
});

// ===================================
// SUPPLIERS_LIST - Filtrado de tabla
// ===================================
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const filterType = document.getElementById('filterType');
    const table = document.getElementById('suppliersTable');

    if (searchInput && filterType && table) {
        const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

        function filterSuppliersTable() {
            const searchTerm = searchInput.value.toLowerCase();
            const filterValue = filterType.value.toLowerCase();

            for (let i = 0; i < rows.length; i++) {
                const row = rows[i];
                // Verificar que la fila tenga celdas (evitar la fila "No hay proveedores")
                if (row.cells.length > 1) {
                    const rut = row.cells[0] ? row.cells[0].textContent.toLowerCase() : '';
                    const empresa = row.cells[1] ? row.cells[1].textContent.toLowerCase() : '';
                    const encargado = row.cells[2] ? row.cells[2].textContent.toLowerCase() : '';
                    const email = row.cells[3] ? row.cells[3].textContent.toLowerCase() : '';

                    const matchesSearch = rut.includes(searchTerm) ||
                        empresa.includes(searchTerm) ||
                        encargado.includes(searchTerm) ||
                        email.includes(searchTerm);
                    const matchesFilter = filterValue === '' || empresa === filterValue;

                    if (matchesSearch && matchesFilter) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                }
            }
        }

        searchInput.addEventListener('keyup', filterSuppliersTable);
        filterType.addEventListener('change', filterSuppliersTable);
    }
});

const filterUser = document.getElementById('filterUser');
if (filterUser) {
    filterUser.addEventListener('change', function() {
        filtrarHistorial();
    });
}

function filtrarHistorial() {
    const filterType = document.getElementById('filterType').value;
    const filterUser = document.getElementById('filterUser').value;
    const searchInput = document.getElementById('searchInput').value;
    
    // Aplicar filtros según tus necesidades
    // Ejemplo de AJAX call o filtrado del DOM
}

// ===================================
// USERS TABLE - Filtrado en tiempo real (Simplified version)
// ===================================
// ===================================
// USERS PAGE - Búsqueda y filtrado (implementado en template)
// ===================================
// Nota: La funcionalidad de búsqueda de usuarios está implementada
// directamente en el template users.html para mejor compatibilidad
// ===================================
// USER EDIT FORM - Password match validation (solo coincidencia, longitud solo backend)
document.addEventListener('DOMContentLoaded', function () {
    const userEditForm = document.querySelector('.add-product-form');
    if (!userEditForm) return;
    const password1 = document.getElementById('new_password');
    const password2 = document.getElementById('new_password2');
    const errorSpan = document.getElementById('password2-error');

    // Validar solo coincidencia de contraseñas
    if (password1 && password2 && errorSpan) {
        userEditForm.addEventListener('submit', function (e) {
            if (password1.value || password2.value) {
                if (!password1.value || !password2.value) {
                    e.preventDefault();
                    errorSpan.textContent = 'Debe completar ambos campos.';
                    errorSpan.style.display = 'block';
                    if (!password1.value) password1.focus();
                    else password2.focus();
                    return false;
                }
                if (password1.value !== password2.value) {
                    e.preventDefault();
                    errorSpan.textContent = 'Las contraseñas no coinciden.';
                    errorSpan.style.display = 'block';
                    password2.focus();
                    return false;
                }
            } else {
                // Ambos campos vacíos: permitir submit
                errorSpan.textContent = '';
                errorSpan.style.display = 'none';
            }
        });
        // Ocultar error al escribir
        password2.addEventListener('input', function () {
            errorSpan.textContent = '';
            errorSpan.style.display = 'none';
        });
        password1.addEventListener('input', function () {
            errorSpan.textContent = '';
            errorSpan.style.display = 'none';
        });
    }
});

// USER EDIT FORM - Toast for Django messages (error only)
document.addEventListener('DOMContentLoaded', function () {
    // Find hidden Django alert messages (error only)
    const alertMessages = document.querySelectorAll('.alert-messages .alert');
    if (alertMessages.length > 0) {
        alertMessages.forEach(function(alert) {
            // Show toast for any message with 'alert' class (Django uses alert-danger for errors)
            if (alert.classList.contains('alert-danger') || alert.classList.contains('alert-error') || alert.classList.contains('alert')) {
                showErrorToast(alert.textContent.trim());
            }
        });
    }
});

function showErrorToast(msg) {
    const toast = document.getElementById('errorToast');
    const toastMsg = document.getElementById('errorToastMsg');
    if (toast && toastMsg) {
        toastMsg.textContent = msg;
        toast.style.display = 'block';
        setTimeout(() => {
            toast.style.display = 'none';
        }, 3500);
    }
}

// ===================================
// CSRF - Obtener token
// ===================================
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    return '';
}



// Cart panel open/close logic and cart logic
// Cart slide panel open/close and item display only
document.addEventListener('DOMContentLoaded', function() {
  const btn = document.getElementById('slideout-btn');
  const panel = document.getElementById('slideout-panel');
  const closeBtn = document.getElementById('close-slideout');
  if (!btn || !panel || !closeBtn) return;

  btn.addEventListener('click', function() {
    panel.style.transform = 'translateX(0)';
    panel.style.visibility = 'visible';
    panel.style.transition = 'transform 0.4s cubic-bezier(.77,0,.18,1), visibility 0s';
    renderCart();
  });
  function hidePanel() {
    panel.style.transform = 'translateX(100%)';
    panel.style.transition = 'transform 0.4s cubic-bezier(.77,0,.18,1), visibility 0s linear 0.4s';
    setTimeout(function() {
      if (panel.style.transform === 'translateX(100%)') panel.style.visibility = 'hidden';
    }, 400);
  }
  closeBtn.addEventListener('click', hidePanel);
  document.addEventListener('mousedown', function(e) {
    if (panel.style.transform === 'translateX(0)' && !panel.contains(e.target) && e.target !== btn) {
      hidePanel();
    }
  });

  // Only display items in the cart (no add/remove/qty/checkout logic)
  const cartList = document.getElementById('cart_items_list');
  if (!panel || !cartList) return;
  function getCart() {
    try {
      return JSON.parse(localStorage.getItem('cart_items') || '{}');
    } catch { return {}; }
  }
  function renderCart() {
    const cart = getCart();
    cartList.innerHTML = '';
    let total = 0;
    for (const [id, data] of Object.entries(cart)) {
      const li = document.createElement('li');
      li.style.display = 'flex';
      li.style.alignItems = 'center';
      li.style.justifyContent = 'space-between';
      li.style.padding = '7px 0 7px 0';
      li.style.borderBottom = '1px solid #e3e8ee';
      li.style.flexWrap = 'nowrap';
      li.style.overflow = 'hidden';
      li.style.textOverflow = 'ellipsis';
      // Remove button (left side)
      const removeBtn = document.createElement('button');
      removeBtn.className = 'cart-remove-btn';
      removeBtn.setAttribute('data-remove-id', id);
      removeBtn.title = 'Quitar del carrito';
      removeBtn.style.background = 'none';
      removeBtn.style.border = 'none';
      removeBtn.style.color = '#c0392b';
      removeBtn.style.fontSize = '1.1em';
      removeBtn.style.marginRight = '7px';
      removeBtn.style.cursor = 'pointer';
      removeBtn.style.lineHeight = '1';
      removeBtn.style.padding = '0 4px';
      removeBtn.textContent = '×';

      // Quantity controls
      const minusBtn = document.createElement('button');
      minusBtn.textContent = '-';
      minusBtn.className = 'cart-qty-btn';
      minusBtn.setAttribute('data-qty-action', 'decrease');
      minusBtn.setAttribute('data-qty-id', id);
      minusBtn.style.background = '#e3e8ee';
      minusBtn.style.border = 'none';
      minusBtn.style.color = '#354e66';
      minusBtn.style.fontWeight = 'bold';
      minusBtn.style.fontSize = '1.1em';
      minusBtn.style.width = '28px';
      minusBtn.style.height = '28px';
      minusBtn.style.borderRadius = '50%';
      minusBtn.style.margin = '0 4px 0 10px';
      minusBtn.style.cursor = 'pointer';

      const plusBtn = document.createElement('button');
      plusBtn.textContent = '+';
      plusBtn.className = 'cart-qty-btn';
      plusBtn.setAttribute('data-qty-action', 'increase');
      plusBtn.setAttribute('data-qty-id', id);
      plusBtn.style.background = '#e3e8ee';
      plusBtn.style.border = 'none';
      plusBtn.style.color = '#354e66';
      plusBtn.style.fontWeight = 'bold';
      plusBtn.style.fontSize = '1.1em';
      plusBtn.style.width = '28px';
      plusBtn.style.height = '28px';
      plusBtn.style.borderRadius = '50%';
      plusBtn.style.margin = '0 0 0 4px';
      plusBtn.style.cursor = 'pointer';

      // Name
      const nameSpan = document.createElement('span');
      nameSpan.style.fontWeight = '500';
      nameSpan.style.color = '#2a3a4d';
      nameSpan.style.whiteSpace = 'nowrap';
      nameSpan.style.overflow = 'hidden';
      nameSpan.style.textOverflow = 'ellipsis';
      nameSpan.style.maxWidth = '60%';
      nameSpan.style.display = 'inline-block';
      nameSpan.textContent = data.name;
      // Price/qty
      const priceSpan = document.createElement('span');
      priceSpan.style.color = '#354e66';
      priceSpan.style.fontWeight = '600';
      priceSpan.style.whiteSpace = 'nowrap';
      priceSpan.style.marginLeft = 'auto';
      priceSpan.innerHTML = `$${parseFloat(data.price).toLocaleString()}`;

      // Quantity controls wrapper
      const qtyWrap = document.createElement('span');
      qtyWrap.style.display = 'inline-flex';
      qtyWrap.style.alignItems = 'center';
      qtyWrap.appendChild(minusBtn);
      const qtyNum = document.createElement('span');
      qtyNum.textContent = data.quantity;
      qtyNum.style.margin = '0 4px';
      qtyNum.style.minWidth = '18px';
      qtyNum.style.textAlign = 'center';
      qtyNum.style.fontWeight = '600';
      qtyWrap.appendChild(qtyNum);
      qtyWrap.appendChild(plusBtn);

      li.appendChild(removeBtn);
      li.appendChild(nameSpan);
      li.appendChild(priceSpan);
      li.appendChild(qtyWrap);
      cartList.appendChild(li);
      // Calculate total
      const priceNum = parseFloat(data.price);
      if (!isNaN(priceNum)) {
        total += priceNum * data.quantity;
      }
    }
    // Update total
    const totalDiv = document.getElementById('cart_total_amount');
    if (totalDiv) {
      totalDiv.innerHTML = `Total: <span style='color:#354e66;'>$${total.toLocaleString()}</span>`;
    }
  }

  // Add back quantity controls and remove event
  document.body.addEventListener('click', function(e) {
    const qtyBtn = e.target.closest('.cart-qty-btn');
    if (qtyBtn && qtyBtn.hasAttribute('data-qty-action') && qtyBtn.hasAttribute('data-qty-id')) {
      const action = qtyBtn.getAttribute('data-qty-action');
      const id = qtyBtn.getAttribute('data-qty-id');
      let cart = getCart();
      let stockNum = cart[id] && cart[id].stock !== undefined && cart[id].stock !== null && cart[id].stock !== '' && cart[id].stock !== 'null' ? parseInt(cart[id].stock, 10) : null;
      if (cart[id]) {
        if (action === 'increase') {
          if (stockNum === null || cart[id].quantity < stockNum) {
            cart[id].quantity += 1;
          }
        } else if (action === 'decrease') {
          if (cart[id].quantity > 1) {
            cart[id].quantity -= 1;
          }
        }
        localStorage.setItem('cart_items', JSON.stringify(cart));
        renderCart();
      }
      return;
    }
    // Remove from cart
    const removeBtn = e.target.closest('.cart-remove-btn');
    if (removeBtn && removeBtn.hasAttribute('data-remove-id')) {
      const id = removeBtn.getAttribute('data-remove-id');
      let cart = getCart();
      if (cart[id]) {
        delete cart[id];
        localStorage.setItem('cart_items', JSON.stringify(cart));
        renderCart();
      }
      return;
    }
    // Add to cart from product button
    const btn = e.target.closest('.cart-inv-btn');
    if (btn && btn.hasAttribute('data-product-id')) {
      e.preventDefault();
      const id = btn.getAttribute('data-product-id');
      const name = btn.getAttribute('data-product-name');
      const price = btn.getAttribute('data-product-price');
      const stock = btn.getAttribute('data-product-stock');
      if (id && name && price) {
        const stockNum = stock !== undefined && stock !== null && stock !== '' ? parseInt(stock, 10) : null;
        let cart = getCart();
        if (cart[id]) {
          if (stockNum === null || cart[id].quantity < stockNum) {
            cart[id].quantity += 1;
          }
        } else {
          cart[id] = { id: id, name: name, price: price, quantity: 1, stock: stock };
        }
        localStorage.setItem('cart_items', JSON.stringify(cart));
        renderCart();
      } else if (!id) {
        alert('Error: el producto no tiene ID. Contacte al administrador.');
      }
    }
  });
  // Render cart on load (from localStorage)
  renderCart();
});

// Checkout: send cart to backend (must be inside DOMContentLoaded for cart panel)
document.addEventListener('DOMContentLoaded', function() {
  const checkoutBtn = document.getElementById('cart-checkout-btn');
  const cartCodeInput = document.getElementById('cart-code-input');
  if (checkoutBtn) {
    checkoutBtn.addEventListener('click', async function() {
      let getCart = window.getCart;
      let renderCart = window.renderCart;
      if (!getCart) {
        getCart = function() {
          try {
            return JSON.parse(localStorage.getItem('cart_items') || '{}');
          } catch { return {}; }
        };
      }
      if (!renderCart) {
        renderCart = function() { window.location.reload(); };
      }
      const cart = getCart();
      const items = Object.values(cart);
      if (!items.length) {
        alert('El carrito está vacío.');
        return;
      }
      const cartCode = cartCodeInput ? cartCodeInput.value.trim() : '';
      if (!cartCode) {
        alert('Debe ingresar el código de la boleta, factura o documento.');
        if (cartCodeInput) cartCodeInput.focus();
        return;
      }
      checkoutBtn.disabled = true;
      checkoutBtn.textContent = 'Procesando...';
      try {
        const resp = await fetch('/cart_checkout/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
          body: JSON.stringify({cart: items, cart_code: cartCode})
        });
        const data = await resp.json();
        if (resp.ok && data.success) {
          localStorage.removeItem('cart_items');
          if (cartCodeInput) cartCodeInput.value = '';
          renderCart();
          alert('¡Movimiento registrado con éxito!');
        } else {
          alert(data.error || 'Error al finalizar la operación.');
        }
      } catch (err) {
        alert('Error de red al finalizar la operación.');
      }
      checkoutBtn.disabled = false;
      checkoutBtn.textContent = 'Finalizar compra';
    });
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const motivoSelect = document.getElementById('id_motivo');
  const boletaInput = document.getElementById('id_boleta_codigo');
  if (motivoSelect && boletaInput) {
    function toggleBoletaInput() {
      if (motivoSelect.value === 'Venta') {
        boletaInput.style.display = '';
        boletaInput.required = true;
      } else {
        boletaInput.style.display = 'none';
        boletaInput.required = false;
        boletaInput.value = '';
      }
    }
    motivoSelect.addEventListener('change', toggleBoletaInput);
    toggleBoletaInput(); // Inicial
  }
});

// ===================================
// HISTORIAL - Toggle between historial and cart sales
// ===================================
let showingCartSales = false;

function toggleCartSalesView() {
    const tablaContainer = document.getElementById("tablaHistorial");
    const showCartSalesBtn = document.getElementById("showCartSalesBtn");
    
    if (!showingCartSales) {
        // Switch to cart sales view
        fetch('/tabla_cart_sales/')
            .then(response => response.text())
            .then(data => {
                tablaContainer.innerHTML = data;
                showingCartSales = true;
                
                // Update button appearance
                showCartSalesBtn.classList.add('active');
                showCartSalesBtn.title = "Mostrar Historial";
                
                // RE-INICIALIZAR el botón toggle
                initializeToggleButton();
            })
            .catch(error => {
                console.error('Error loading cart sales:', error);
            });
    } else {
        // Switch back to historial view
        fetch('/tabla_historial/')
            .then(response => response.text())
            .then(data => {
                tablaContainer.innerHTML = data;
                showingCartSales = false;
                
                // Update button appearance
                showCartSalesBtn.classList.remove('active');
                showCartSalesBtn.title = "Mostrar Ventas del Carrito";
                
                // RE-INICIALIZAR el botón toggle
                initializeToggleButton();
            })
            .catch(error => {
                console.error('Error loading historial:', error);
            });
    }
}

// Initialize cart sales button when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Only add functionality on historial page
    if (window.location.pathname.includes('/historial')) {
        const showCartSalesBtn = document.getElementById("showCartSalesBtn");
        if (showCartSalesBtn) {
            showCartSalesBtn.addEventListener('click', function(e) {
                e.preventDefault();
                toggleCartSalesView();
            });
            
            // Set initial title
            showCartSalesBtn.title = "Mostrar Ventas del Carrito";
        }
    }
});