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
    
    // Configurar el panel flotante de accesibilidad
    setupAccessibilityFloatingPanel();
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
    
    // Botón para silenciar asistente de voz en la barra de navegación
    const voiceMuteButton = document.getElementById('toggle-voice-mute');
    if (voiceMuteButton) {
        // Eliminar cualquier listener previo
        voiceMuteButton.removeEventListener('click', handleNavbarMuteToggle);
        
        // Función para manejar el clic
        function handleNavbarMuteToggle(e) {
            e.preventDefault();
            
            // Verificar si la función toggleMute existe
            if (typeof toggleMute === 'function') {
                toggleMute(); // Esta función ahora maneja toda la actualización visual
            } else {
                console.warn('La función toggleMute no está disponible');
                alert('El asistente de voz no está disponible. Intenta actualizar la página.');
            }
        }
        
        // Agregar nuevo listener
        voiceMuteButton.addEventListener('click', handleNavbarMuteToggle);
        
        // Inicializar estado del botón
        if (typeof updateMuteVisualState === 'function') {
            updateMuteVisualState();
        } else {
            updateNavbarMuteIcon(); // Función local como fallback
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

/**
 * Guarda las configuraciones de accesibilidad en el almacenamiento local
 */
function saveAccessibilitySettings() {
    localStorage.setItem('highContrast', document.body.classList.contains('high-contrast'));
    
    if (document.body.classList.contains('text-lg')) {
        localStorage.setItem('fontSize', 'text-lg');
    } else if (document.body.classList.contains('text-xl')) {
        localStorage.setItem('fontSize', 'text-xl');
    } else {
        localStorage.setItem('fontSize', '');
    }
}

/**
 * Actualiza el ícono del botón de silencio en la barra de navegación
 * basado en el estado actual guardado en localStorage
 */
function updateNavbarMuteIcon() {
    const voiceMuteButton = document.getElementById('toggle-voice-mute');
    if (!voiceMuteButton) return;
    
    const isMuted = localStorage.getItem('voiceAssistant_muted') === 'true';
    
    if (isMuted) {
        voiceMuteButton.innerHTML = '<i class="bi bi-volume-mute"></i>';
        voiceMuteButton.title = 'Activar asistente de voz';
        voiceMuteButton.setAttribute('aria-label', 'Activar asistente de voz');
    } else {
        voiceMuteButton.innerHTML = '<i class="bi bi-volume-up"></i>';
        voiceMuteButton.title = 'Silenciar asistente de voz';
        voiceMuteButton.setAttribute('aria-label', 'Silenciar asistente de voz');
    }
}

/**
 * Configura el panel flotante de herramientas de accesibilidad
 */
function setupAccessibilityFloatingPanel() {
    const toggleBtn = document.getElementById('accessibility-toggle');
    const toolsContent = document.getElementById('accessibility-tools-content');
    
    if (!toggleBtn || !toolsContent) return;
    
    // Eliminar cualquier listener previo para evitar duplicados (por si acaso)
    toggleBtn.removeEventListener('click', toggleAccessibilityPanel);
    
    // Función separada para el manejo del panel
    function toggleAccessibilityPanel(e) {
        e.preventDefault();
        e.stopPropagation(); // Evitar propagación
        
        // Si el panel está visible, ocultarlo; si no, mostrarlo
        if (toolsContent.classList.contains('show')) {
            toolsContent.classList.remove('show');
            toggleBtn.setAttribute('aria-expanded', 'false');
            announceForScreenReader('Panel de herramientas de accesibilidad cerrado');
        } else {
            toolsContent.classList.add('show');
            toggleBtn.setAttribute('aria-expanded', 'true');
            announceForScreenReader('Panel de herramientas de accesibilidad abierto');
        }
    }
    
    // Agregar listener al botón con la función separada
    toggleBtn.addEventListener('click', toggleAccessibilityPanel);
    
    // Mejorar el manejo de clics fuera del panel
    document.addEventListener('click', function(e) {
        // Solo actuar si el panel está visible y se hace clic fuera
        if (toolsContent.classList.contains('show') && 
            !toolsContent.contains(e.target) && 
            e.target !== toggleBtn) {
            toolsContent.classList.remove('show');
            toggleBtn.setAttribute('aria-expanded', 'false');
        }
    });
    
    // Configurar botones del panel
    const contrastBtn = document.getElementById('accessibility-contrast');
    const fontSizeBtn = document.getElementById('accessibility-text-increase');
    const voiceToggleBtn = document.getElementById('accessibility-voice-toggle');
    
    // Botón de contraste
    if (contrastBtn) {
        contrastBtn.addEventListener('click', toggleHighContrast);
        // Sincronizar estado visual
        updateButtonState(contrastBtn, 'highContrast');
    }
    
    // Botón de tamaño de texto
    if (fontSizeBtn) {
        fontSizeBtn.addEventListener('click', toggleFontSize);
    }
    
    // Botón de asistente de voz
    if (voiceToggleBtn) {
        // Eliminar listeners previos
        voiceToggleBtn.removeEventListener('click', handleVoiceToggle);
        
        // Función para manejar el clic en el botón de silenciar
        function handleVoiceToggle(e) {
            e.preventDefault();
            e.stopPropagation(); // Evitar que el clic cierre el panel
            
            if (typeof toggleMute === 'function') {
                toggleMute();
                // La actualización visual se maneja dentro de toggleMute
            } else {
                console.warn('La función toggleMute no está disponible');
                alert('No se puede cambiar el estado del asistente de voz. Intenta actualizar la página.');
            }
        }
        
        // Agregar nuevo listener
        voiceToggleBtn.addEventListener('click', handleVoiceToggle);
        
        // Actualizar estado visual inicial
        if (typeof updateMuteVisualState === 'function') {
            updateMuteVisualState();
        } else {
            updateVoiceToggleState(); // Función local como fallback
        }
    }
}

/**
 * Actualiza el estado visual del botón de alternar voz
 */
function updateVoiceToggleState() {
    const voiceToggleBtn = document.getElementById('accessibility-voice-toggle');
    const voiceToggleText = document.getElementById('voice-toggle-text');
    
    if (!voiceToggleBtn || !voiceToggleText) return;
    
    const isMuted = localStorage.getItem('voiceAssistant_muted') === 'true';
    
    if (isMuted) {
        voiceToggleBtn.innerHTML = '<i class="bi bi-volume-mute me-2"></i> Activar voz';
        voiceToggleBtn.setAttribute('aria-label', 'Activar asistente de voz');
    } else {
        voiceToggleBtn.innerHTML = '<i class="bi bi-volume-up me-2"></i> Silenciar voz';
        voiceToggleBtn.setAttribute('aria-label', 'Silenciar asistente de voz');
    }
}

/**
 * Actualiza el estado visual de un botón según su configuración
 */
function updateButtonState(button, settingName) {
    const isActive = localStorage.getItem(settingName) === 'true';
    if (isActive) {
        button.classList.add('btn-primary');
        button.classList.remove('btn-outline-primary');
    } else {
        button.classList.add('btn-outline-primary');
        button.classList.remove('btn-primary');
    }
}
