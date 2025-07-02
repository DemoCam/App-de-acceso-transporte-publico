/**
 * Funciones globales para el asistente de voz
 * Este archivo contiene funciones que necesitan ser accesibles desde
 * diferentes archivos JavaScript como accesibilidad.js
 */

// Variables globales para el estado del asistente
window.voiceAssistant = {
    muted: localStorage.getItem('voiceAssistant_muted') === 'true',
    autoDescribe: localStorage.getItem('autoDescribePage') === 'true'
};

/**
 * Alterna el estado de silencio del asistente de voz
 * Esta función es llamada desde los botones de la interfaz
 * @returns {boolean} - El nuevo estado (true = activado, false = silenciado)
 */
function toggleMute() {
    // Invertir el estado actual
    window.voiceAssistant.muted = !window.voiceAssistant.muted;
    
    // Guardar en localStorage
    localStorage.setItem('voiceAssistant_muted', window.voiceAssistant.muted);
    
    // Mensaje de confirmación para el usuario
    const voiceOutputElement = document.getElementById('voice-output');
    if (voiceOutputElement) {
        if (!window.voiceAssistant.muted) {
            // Si estaba silenciado, ahora no lo está
            voiceOutputElement.textContent = 'Asistente de voz activado';
            voiceOutputElement.style.display = 'block';
            
            // Usar speechSynthesis directamente para este mensaje
            if (window.speechSynthesis) {
                const utterance = new SpeechSynthesisUtterance('Asistente de voz activado');
                utterance.lang = 'es-ES';
                window.speechSynthesis.speak(utterance);
            }
        } else {
            // Si no estaba silenciado, ahora sí
            voiceOutputElement.textContent = 'Asistente de voz silenciado';
            voiceOutputElement.style.display = 'block';
        }
        
        // Ocultar el mensaje después de un tiempo
        setTimeout(() => {
            voiceOutputElement.style.display = 'none';
        }, 3000);
    }
    
    // Actualizar el estado visual de los botones
    updateMuteVisualState();
    
    return !window.voiceAssistant.muted; // true = activado, false = silenciado
}

/**
 * Verifica si el asistente de voz está silenciado
 * @returns {boolean} - true si está silenciado, false si no
 */
function isVoiceAssistantMuted() {
    return window.voiceAssistant.muted;
}

/**
 * Actualiza el estado visual de todos los botones relacionados con silenciar
 * tanto en la barra de navegación como en el panel de accesibilidad
 */
function updateMuteVisualState() {
    const isMuted = isVoiceAssistantMuted();
    
    // Actualizar el botón en la barra de navegación
    const navbarMuteButton = document.getElementById('toggle-voice-mute');
    if (navbarMuteButton) {
        if (isMuted) {
            navbarMuteButton.innerHTML = '<i class="bi bi-volume-mute"></i>';
            navbarMuteButton.title = 'Activar asistente de voz';
            navbarMuteButton.setAttribute('aria-label', 'Activar asistente de voz');
        } else {
            navbarMuteButton.innerHTML = '<i class="bi bi-volume-up"></i>';
            navbarMuteButton.title = 'Silenciar asistente de voz';
            navbarMuteButton.setAttribute('aria-label', 'Silenciar asistente de voz');
        }
    }
    
    // Actualizar el botón en el panel de accesibilidad
    const accessibilityVoiceToggle = document.getElementById('accessibility-voice-toggle');
    if (accessibilityVoiceToggle) {
        if (isMuted) {
            accessibilityVoiceToggle.innerHTML = '<i class="bi bi-volume-mute me-2"></i> Activar voz';
        } else {
            accessibilityVoiceToggle.innerHTML = '<i class="bi bi-volume-up me-2"></i> Silenciar voz';
        }
    }
}

/**
 * Guarda las preferencias de accesibilidad del usuario
 * @param {boolean} autoDescribe - Si las páginas deben describirse automáticamente
 */
function saveAccessibilityPrefs(autoDescribe) {
    window.voiceAssistant.autoDescribe = autoDescribe;
    localStorage.setItem('autoDescribePage', autoDescribe);
}

/**
 * Comprueba si las páginas deben describirse automáticamente
 * @returns {boolean} - true si debe describirse, false si no
 */
function shouldAutoDescribePage() {
    return window.voiceAssistant.autoDescribe;
}

// Inicializar el estado visual cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    updateMuteVisualState();
});
