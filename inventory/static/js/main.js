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
        });
}

// ===================================
// INVENTARIO - Event listeners
// ===================================
document.addEventListener('DOMContentLoaded', function() {
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
// TABLAS - Toggle columnas alternadas
// ===================================
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.querySelector('.dynamic-table-button');
    const table = document.querySelector('.table');
    
    if (toggleButton && table) {
        let stripedColumns = false;
        
        // SVG para estado inactivo (bombilla apagada)
        const inactiveSVG = `<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m4.988 19.012 5.41-5.41m2.366-6.424 4.058 4.058-2.03 5.41L5.3 20 4 18.701l3.355-9.494 5.41-2.029Zm4.626 4.625L12.197 6.61 14.807 4 20 9.194l-2.61 2.61Z"/>
</svg>
`;
        
        // SVG para estado activo (bombilla encendida)
        const activeSVG = `<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor" viewBox="0 0 24 24">
  <path fill-rule="evenodd" d="M15.514 3.293a1 1 0 0 0-1.415 0L12.151 5.24a.93.93 0 0 1 .056.052l6.5 6.5a.97.97 0 0 1 .052.056L20.707 9.9a1 1 0 0 0 0-1.415l-5.193-5.193ZM7.004 8.27l3.892-1.46 6.293 6.293-1.46 3.893a1 1 0 0 1-.603.591l-9.494 3.355a1 1 0 0 1-.98-.18l6.452-6.453a1 1 0 0 0-1.414-1.414l-6.453 6.452a1 1 0 0 1-.18-.98l3.355-9.494a1 1 0 0 1 .591-.603Z" clip-rule="evenodd"/>
</svg>
`;
        
        // Estado inicial
        toggleButton.innerHTML = inactiveSVG;
        
        toggleButton.addEventListener('click', function(e) {
            e.preventDefault();
            stripedColumns = !stripedColumns;
            
            if (stripedColumns) {
                table.classList.add('striped-columns');
                toggleButton.innerHTML = activeSVG;
                toggleButton.classList.add('active');
            } else {
                table.classList.remove('striped-columns');
                toggleButton.innerHTML = inactiveSVG;
                toggleButton.classList.remove('active');
            }
        });
    }
});


// ===================================
// EDIT_ITEM - Manejo de motivos
// ===================================
document.addEventListener('DOMContentLoaded', function() {
  const motivoSelect = document.getElementById('id_motivo');
  const motivoExtra = document.getElementById('motivo_extra');
  const motivoHidden = document.getElementById('motivo_hidden');
  const form = document.querySelector('form');

  motivoSelect.addEventListener('change', function() {
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

  form.addEventListener('submit', function(e) {
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
});


// ===================================
// HISTORIAL - Actualización de tabla
// ===================================
function updateHistorialTable() {
    const query = document.getElementById("searchInput").value;
    const type = document.getElementById("filterType").value;
    const startDateInput = document.getElementById("startDate");
    const endDateInput = document.getElementById("endDate");
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;

    // Validar si las fechas están bien puestas
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
            });

        return; 
    }

    let url = '/historial/?';

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
        });
}

// ===================================
// HISTORIAL - Event listeners
// ===================================
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById("searchInput");
    const filterType = document.getElementById("filterType");
    const startDate = document.getElementById("startDate");
    const endDate = document.getElementById("endDate");
    
    if (searchInput && document.getElementById("tablaHistorial")) {
        searchInput.addEventListener("input", updateHistorialTable);
    }
    
    if (filterType && document.getElementById("tablaHistorial")) {
        filterType.addEventListener("change", updateHistorialTable);
    }
    
    if (startDate && document.getElementById("tablaHistorial")) {
        startDate.addEventListener("change", updateHistorialTable);
    }
    
    if (endDate && document.getElementById("tablaHistorial")) {
        endDate.addEventListener("change", updateHistorialTable);
    }
});



// ===================================
// REGISTER - Generar contraseña
// ===================================
function enablePassword() {
    const passwordField = document.getElementById('id_password1');
    const confirmField = document.getElementById('id_password2');

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
    const passwordField = document.getElementById('id_password1');
    if (passwordField.value) {
        passwordField.select();
        document.execCommand('copy');

        // Mostrar toast flotante
        const toast = document.getElementById('copyToast');
        if (toast) {
            toast.style.display = 'block';
            setTimeout(() => {
                toast.style.display = 'none';
            }, 2000);
        }
    }
}

// ===================================
// REGISTER - Toggle visibilidad contraseña
// ===================================
function togglePasswordVisibility() {
    const passwordField = document.getElementById('id_password1');
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
document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.querySelector('form[method="POST"]');
    
    if (registerForm && document.getElementById('id_username')) {
        registerForm.addEventListener('submit', function(e) {
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
// SUPPLIERS_FORM - Formateo de RUT
// ===================================
document.addEventListener('DOMContentLoaded', function() {
    const rutInput = document.getElementById('id_rut');
    
    if (rutInput) {
        rutInput.addEventListener('input', function() {
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
        rutInput.addEventListener('blur', function() {
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
// SUPPLIERS_LIST - Filtrado de tabla
// ===================================
document.addEventListener('DOMContentLoaded', function() {
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



