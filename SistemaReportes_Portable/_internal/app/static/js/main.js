// Funciones globales de la aplicación

// ===== PREFERENCES =====
document.addEventListener('DOMContentLoaded', function() {
    initializePreferences();
});

function initializePreferences() {
    // Load saved preferences from localStorage
    const savedTheme = localStorage.getItem('theme') || 'light';
    const savedFontSize = localStorage.getItem('fontSize') || 'medium';
    const savedLanguage = localStorage.getItem('language') || 'es';
    
    // Apply saved preferences
    applyTheme(savedTheme);
    applyFontSize(savedFontSize);
    applyLanguage(savedLanguage);
    
    // Attach event listeners
    document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
    document.getElementById('font-small').addEventListener('click', () => setFontSize('small'));
    document.getElementById('font-medium').addEventListener('click', () => setFontSize('medium'));
    document.getElementById('font-large').addEventListener('click', () => setFontSize('large'));
    document.getElementById('language-select').addEventListener('change', (e) => setLanguage(e.target.value));
}

function toggleTheme() {
    const body = document.body;
    if (body.classList.contains('dark-mode')) {
        applyTheme('light');
    } else {
        applyTheme('dark');
    }
}

function applyTheme(theme) {
    const body = document.body;
    if (theme === 'dark') {
        body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
    } else {
        body.classList.remove('dark-mode');
        localStorage.setItem('theme', 'light');
    }
}

function setFontSize(size) {
    const body = document.body;
    body.classList.remove('font-small', 'font-medium', 'font-large');
    
    if (size === 'small') {
        body.classList.add('font-small');
    } else if (size === 'large') {
        body.classList.add('font-large');
    }
    
    // Update button states
    document.getElementById('font-small').classList.toggle('active', size === 'small');
    document.getElementById('font-medium').classList.toggle('active', size === 'medium');
    document.getElementById('font-large').classList.toggle('active', size === 'large');
    
    localStorage.setItem('fontSize', size);
}

function applyFontSize(size) {
    const body = document.body;
    body.classList.remove('font-small', 'font-medium', 'font-large');
    
    if (size === 'small') {
        body.classList.add('font-small');
        document.getElementById('font-small').classList.add('active');
    } else if (size === 'large') {
        body.classList.add('font-large');
        document.getElementById('font-large').classList.add('active');
    } else {
        document.getElementById('font-medium').classList.add('active');
    }
}

function setLanguage(lang) {
    localStorage.setItem('language', lang);
    document.documentElement.lang = lang;
    applyLanguage(lang);
}

function applyLanguage(lang) {
    document.documentElement.lang = lang;
    const langSelect = document.getElementById('language-select');
    if (langSelect) {
        langSelect.value = lang;
    }
    
    const translations = {
        'es': {
            'Tamaño:': 'Tamaño:',
            'Contraste:': 'Contraste:',
            'Idioma:': 'Idioma:',
            'Inicio': 'Inicio',
            'Cargar Excel': 'Cargar Excel',
            'Reportes': 'Reportes',
            'Dashboard': 'Dashboard',
            'Cerrar Sesión': 'Cerrar Sesión',
            'Iniciar Sesión': 'Iniciar Sesión',
            'Registrarse': 'Registrarse',
            'Gestiona tus Reportes REDEMI': 'Gestiona tus Reportes REDEMI',
            'Simple. Rápido. Profesional.': 'Simple. Rápido. Profesional.',
            'Subir Archivos': 'Subir Archivos',
            'Carga Fácil': 'Carga Fácil',
            'Importa Excel en un click': 'Importa Excel en un click',
            'Análisis Rápido': 'Análisis Rápido',
            'Procesa al instante': 'Procesa al instante',
            'Exporta Todo': 'Exporta Todo',
            'Descarga en Excel': 'Descarga en Excel'
        },
        'en': {
            'Tamaño:': 'Size:',
            'Contraste:': 'Contrast:',
            'Idioma:': 'Language:',
            'Inicio': 'Home',
            'Cargar Excel': 'Load Excel',
            'Reportes': 'Reports',
            'Dashboard': 'Dashboard',
            'Cerrar Sesión': 'Logout',
            'Iniciar Sesión': 'Login',
            'Registrarse': 'Register',
            'Gestiona tus Reportes REDEMI': 'Manage your REDEMI Reports',
            'Simple. Rápido. Profesional.': 'Simple. Fast. Professional.',
            'Subir Archivos': 'Upload Files',
            'Carga Fácil': 'Easy Upload',
            'Importa Excel en un click': 'Import Excel in one click',
            'Análisis Rápido': 'Fast Analysis',
            'Procesa al instante': 'Process instantly',
            'Exporta Todo': 'Export Everything',
            'Descarga en Excel': 'Download as Excel'
        }
    };
    
    // Translate all elements with data-i18n attribute
    const elementsToTranslate = document.querySelectorAll('[data-i18n]');
    elementsToTranslate.forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });
}

/**
 * Navega a una sección específica
 */
function goToSection(sectionName) {
    // Ocultar todas las secciones
    const sections = document.querySelectorAll('.section');
    sections.forEach(s => s.classList.remove('active'));

    // Mostrar sección activa
    const activeSection = document.getElementById(sectionName + '-section');
    if (activeSection) {
        activeSection.classList.add('active');
    }

    // Cargar contenido según la sección
    if (sectionName === 'reportes') {
        loadReportesPage();
    } else if (sectionName === 'dashboard') {
        loadDashboardPage();
    }
}

/**
 * Carga la página de reportes
 */
function loadReportesPage() {
    fetch('/reportes')
        .then(response => response.text())
        .then(html => {
            document.body.innerHTML = html;
        })
        .catch(error => console.error('Error:', error));
}

/**
 * Carga la página del dashboard
 */
function loadDashboardPage() {
    fetch('/dashboard')
        .then(response => response.text())
        .then(html => {
            document.body.innerHTML = html;
        })
        .catch(error => console.error('Error:', error));
}

/**
 * Formatea un número con decimales especificados y separadores de miles
 */
function formatNumber(num, decimales = 2) {
    const factor = Math.pow(10, decimales);
    const rounded = Math.round(num * factor) / factor;
    const formatted = rounded.toFixed(decimales);
    
    // Separar enteros de decimales
    const [parteEntera, parteDecimal] = formatted.split('.');
    
    // Agregar puntos cada 3 dígitos en la parte entera
    const conMiles = parteEntera.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    
    // No mostrar decimales si son .00
    if (parteDecimal === '00') {
        return conMiles;
    }
    
    // Retornar con coma como separador decimal
    return `${conMiles},${parteDecimal}`;
}

/**
 * Convierte una fecha a formato legible
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

/**
 * Muestra una notificación
 */
function showNotification(message, type = 'info') {
    const alertClass = {
        'success': 'alert-success',
        'danger': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[type] || 'alert-info';

    const alertHTML = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <strong>${type.charAt(0).toUpperCase() + type.slice(1)}:</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    const container = document.createElement('div');
    container.innerHTML = alertHTML;
    document.body.insertBefore(container.firstElementChild, document.body.firstChild);

    // Auto-dismiss después de 5 segundos
    setTimeout(() => {
        const alert = document.querySelector('.alert');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

/**
 * Carga las estadísticas generales
 */
function loadStats() {
    fetch('/estadisticas')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('total-registros').textContent = formatNumber(data.estadisticas.total_registros, 2);
                document.getElementById('total-usuarios').textContent = formatNumber(data.estadisticas.usuarios_unicos, 2);
                document.getElementById('total-grupos').textContent = formatNumber(data.estadisticas.grupos_unicos, 2);
                document.getElementById('total-horas').textContent = formatNumber(data.estadisticas.total_horas_aprobadas, 2);
            }
        })
        .catch(error => console.error('Error cargando estadísticas:', error));
}

// Cargar estadísticas al cargar la página (solo si existe el dashboard)
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('dashboard-section')) {
        loadStats();
    }
});

/**
 * Validar email
 */
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Formatea bytes a formato legible
 */
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/**
 * Realiza una solicitud AJAX con manejo de errores
 */
async function fetchWithError(url, options = {}) {
    try {
        const response = await fetch(url, options);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        showNotification(`Error: ${error.message}`, 'danger');
        throw error;
    }
}

/**
 * Exporta datos a CSV
 */
function exportToCSV(data, filename) {
    const csv = [
        Object.keys(data[0]).join(','),
        ...data.map(row => Object.values(row).join(','))
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
}

/**
 * Limpia un formulario
 */
function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}

/**
 * Desactiva/activa un botón
 */
function setButtonLoading(buttonId, loading = true) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.disabled = loading;
        const originalText = button.dataset.originalText || button.textContent;

        if (loading) {
            button.dataset.originalText = originalText;
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Cargando...';
        } else {
            button.textContent = originalText;
        }
    }
}

/**
 * Copia texto al portapapeles
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copiado al portapapeles', 'success');
    }).catch(err => {
        showNotification('Error al copiar', 'danger');
    });
}

/**
 * Genera un UUID
 */
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0,
            v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Función de descarga mejorada
function descargarUsuario() {
    const usuario = document.getElementById('usuario').value;
    
    // Validación simple pero clara
    if (!usuario || usuario === '') {
        alert('Por favor, selecciona un usuario primero');
        return;
    }
    
    // Obtener filtros adicionales
    const fechaInicio = document.getElementById('fecha_inicio').value || '';
    const fechaFin = document.getElementById('fecha_fin').value || '';
    const grupo = document.getElementById('grupo').value || 'Todos';
    
    // Construir URL con parámetros
    let url = `/export/usuario/${encodeURIComponent(usuario)}`;
    const params = new URLSearchParams();
    
    if (fechaInicio) params.append('fecha_inicio', fechaInicio);
    if (fechaFin) params.append('fecha_fin', fechaFin);
    if (grupo !== 'Todos') params.append('grupo', grupo);
    
    if (params.toString()) {
        url += '?' + params.toString();
    }
    
    // Descargar
    window.location.href = url;
}

function descargarGlobal() {
    const fechaInicio = document.getElementById('fecha_inicio').value || '';
    const fechaFin = document.getElementById('fecha_fin').value || '';
    const grupo = document.getElementById('grupo').value || 'Todos';
    
    let url = '/export/global';
    const params = new URLSearchParams();
    
    if (fechaInicio) params.append('fecha_inicio', fechaInicio);
    if (fechaFin) params.append('fecha_fin', fechaFin);
    if (grupo !== 'Todos') params.append('grupo', grupo);
    
    if (params.toString()) {
        url += '?' + params.toString();
    }
    
    window.location.href = url;
}
