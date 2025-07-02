/**
 * Funciones de accesibilidad para la aplicación de Transporte Accesible Cali
 */

document.addEventListener('DOMContentLoaded', function() {
    // Botones de accesibilidad
    setupAccessibilityButtons();
    
    // Focus visible en elementos interactivos
    enhanceKeyboardFocus();
    
    // Cargar configuración de accesibilidad guardada
    loadAccessibilitySettings();
});

/**
 * Configura los botones de accesibilidad en la barra de navegación
 */
function setupAccessibilityButtons() {
    // Toggle de alto contraste
    const contrastButton = document.getElementById('toggle-high-contrast');
    if (contrastButton) {
        contrastButton.addEventListener('click', toggleHighContrast);
        
        // Aplicar el estado guardado (si existe)
        if (localStorage.getItem('highContrast') === 'true') {
            document.body.classList.add('high-contrast');
        }
    }
    
    // Toggle de tamaño de texto
    const fontSizeButton = document.getElementById('toggle-font-size');
    if (fontSizeButton) {
        fontSizeButton.addEventListener('click', toggleFontSize);
        
        // Aplicar el estado guardado (si existe)
        const fontSize = localStorage.getItem('fontSize');
        if (fontSize) {
            document.body.classList.add(fontSize);
        }
    }
}

/**
 * Alterna el modo de alto contraste
 */
function toggleHighContrast() {
    const body = document.body;
    body.classList.toggle('high-contrast');
    
    // Guardar preferencia
    localStorage.setItem('highContrast', body.classList.contains('high-contrast'));
    
    // Anuncio para lectores de pantalla
    announceForScreenReader(
        body.classList.contains('high-contrast') 
            ? 'Modo de alto contraste activado' 
            : 'Modo de alto contraste desactivado'
    );
}

/**
 * Alterna el tamaño del texto
 */
function toggleFontSize() {
    const body = document.body;
    
    if (body.classList.contains('large-text')) {
        body.classList.remove('large-text');
        body.classList.add('larger-text');
        localStorage.setItem('fontSize', 'larger-text');
        announceForScreenReader('Tamaño de texto: muy grande');
    } 
    else if (body.classList.contains('larger-text')) {
        body.classList.remove('larger-text');
        localStorage.removeItem('fontSize');
        announceForScreenReader('Tamaño de texto: normal');
    } 
    else {
        body.classList.add('large-text');
        localStorage.setItem('fontSize', 'large-text');
        announceForScreenReader('Tamaño de texto: grande');
    }
}

/**
 * Mejora la visibilidad del foco del teclado
 */
function enhanceKeyboardFocus() {
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-user');
        }
    });
    
    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-user');
    });
}

/**
 * Anuncia un mensaje para lectores de pantalla
 * @param {string} message - El mensaje a anunciar
 */
function announceForScreenReader(message) {
    let srAnnouncer = document.getElementById('sr-announcer');
    
    if (!srAnnouncer) {
        srAnnouncer = document.createElement('div');
        srAnnouncer.id = 'sr-announcer';
        srAnnouncer.setAttribute('aria-live', 'polite');
        srAnnouncer.style.position = 'absolute';
        srAnnouncer.style.width = '1px';
        srAnnouncer.style.height = '1px';
        srAnnouncer.style.padding = '0';
        srAnnouncer.style.overflow = 'hidden';
        srAnnouncer.style.clip = 'rect(0, 0, 0, 0)';
        srAnnouncer.style.whiteSpace = 'nowrap';
        srAnnouncer.style.border = '0';
        document.body.appendChild(srAnnouncer);
    }
    
    srAnnouncer.textContent = message;
}

/**
 * Carga las configuraciones de accesibilidad guardadas
 */
function loadAccessibilitySettings() {
    // Cargar configuración de tamaño de texto
    const savedFontSize = localStorage.getItem('fontSize');
    if (savedFontSize) {
        document.body.classList.add(savedFontSize);
    }
    
    // Cargar configuración de contraste
    const savedContrast = localStorage.getItem('highContrast');
    if (savedContrast === 'true') {
        document.body.classList.add('high-contrast');
    }
    
    // Cargar configuración de animaciones reducidas
    const savedMotion = localStorage.getItem('reducedMotion');
    if (savedMotion === 'true') {
        document.body.classList.add('reduced-motion');
    }
}
