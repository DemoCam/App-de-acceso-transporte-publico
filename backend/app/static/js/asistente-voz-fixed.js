/**
 * Asistente de voz para la aplicación de transporte accesible
 * Permite interactuar con la aplicación mediante comandos de voz
 */

// Inicializar variables para reconocimiento y síntesis de voz
let recognition = null;
let speechSynthesis = window.speechSynthesis;
let isListening = false;
let isMuted = localStorage.getItem('voiceAssistant_muted') === 'true'; // Recuperar estado guardado
let pageDescriptions = {};

// Configurar descripciones de páginas
pageDescriptions = {
    'inicio': 'Bienvenido a Transporte Accesible Cali, tu guía para moverte por la ciudad de manera inclusiva. Aquí puedes consultar rutas, paradas y recibir asistencia para planificar tu viaje.',
    'rutas': 'En esta sección puedes consultar todas las rutas disponibles del transporte público, ver sus frecuencias y horarios. Selecciona una ruta para ver su recorrido detallado.',
    'paradas': 'Aquí encuentras información sobre todas las paradas del sistema de transporte, incluyendo características de accesibilidad, ubicación y las rutas que pasan por cada parada.',
    'ayuda': 'En esta sección encontrarás guías de uso de la aplicación, consejos de accesibilidad y respuestas a preguntas frecuentes sobre el sistema de transporte.',
    'perfil': 'Esta es tu página de perfil personal donde puedes ver y actualizar tu información, revisar tu historial y personalizar tus preferencias.',
    'admin': 'Estás en el panel de administración donde puedes gestionar rutas, paradas, asociaciones entre rutas y paradas, y usuarios del sistema.'
};

// Inicializar el asistente de voz cuando se carga la página
document.addEventListener('DOMContentLoaded', () => {
    // Verificar soporte para reconocimiento de voz
    if ('webkitSpeechRecognition' in window) {
        // Crear objeto de reconocimiento de voz
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'es-ES';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        
        console.log("Reconocimiento de voz soportado (webkitSpeechRecognition)");

        // Configurar eventos para el reconocimiento de voz
        recognition.onresult = handleVoiceCommand;
        recognition.onerror = handleError;
        recognition.onend = () => {
            isListening = false;
            updateVoiceButtonState();
        };

        // Añadir botón de asistente de voz
        setupVoiceAssistant();
        
    } else if ('SpeechRecognition' in window) {
        // Soporte para navegadores que implementan el estándar
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'es-ES';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        
        console.log("Reconocimiento de voz soportado (SpeechRecognition)");
        
        // Configurar eventos para el reconocimiento de voz
        recognition.onresult = handleVoiceCommand;
        recognition.onerror = handleError;
        recognition.onend = () => {
            isListening = false;
            updateVoiceButtonState();
        };

        // Añadir botón de asistente de voz
        setupVoiceAssistant();
    } else {
        console.warn('El reconocimiento de voz no es compatible con este navegador');
        
        // Crear una alerta para informar al usuario
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-warning alert-dismissible fade show';
        alertDiv.setAttribute('role', 'alert');
        alertDiv.innerHTML = `
            <strong>¡Navegador no compatible!</strong> El reconocimiento de voz no está disponible en este navegador. 
            Intente con Chrome, Edge o Safari para usar esta función.
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
        `;
        
        // Insertar al principio del contenido
        setTimeout(() => {
            const content = document.querySelector('.container') || document.querySelector('main') || document.body;
            if (content) {
                content.insertBefore(alertDiv, content.firstChild);
            }
        }, 1000);
    }

    // Mostrar notificación sobre el botón de silencio si es la primera visita
    if (localStorage.getItem('voiceAssistant_infoShown') !== 'true') {
        setTimeout(() => {
            showVoiceOutput('Asistente de voz disponible. Puedes silenciarlo con el botón verde ubicado arriba del botón del micrófono.');
            localStorage.setItem('voiceAssistant_infoShown', 'true');
            setTimeout(() => {
                hideVoiceOutput();
            }, 6000);
        }, 2000);
    }
    
    // Describir la página actual si es la primera visita
    setTimeout(() => {
        if (!isMuted) {
            describeCurrentPage();
        }
    }, 1000);
});

/**
 * Configura el asistente de voz añadiendo botones a la interfaz
 */
function setupVoiceAssistant() {
    // Crear botón flotante para activar asistente
    const voiceButton = document.createElement('button');
    voiceButton.id = 'voice-assistant-btn';
    voiceButton.className = 'voice-btn';
    voiceButton.setAttribute('aria-label', 'Activar asistente de voz');
    voiceButton.innerHTML = '<i class="bi bi-mic"></i>';
    voiceButton.title = 'Asistente de voz (Presiona para hablar)';
    
    // Añadir estilos del botón
    voiceButton.style.position = 'fixed';
    voiceButton.style.bottom = '20px';
    voiceButton.style.right = '20px';
    voiceButton.style.width = '60px';
    voiceButton.style.height = '60px';
    voiceButton.style.borderRadius = '50%';
    voiceButton.style.backgroundColor = '#007bff';
    voiceButton.style.color = 'white';
    voiceButton.style.border = 'none';
    voiceButton.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
    voiceButton.style.zIndex = '1000';
    voiceButton.style.cursor = 'pointer';
    
    // Añadir el botón al DOM
    document.body.appendChild(voiceButton);
    
    // Añadir manejador de eventos para el botón
    voiceButton.addEventListener('click', toggleVoiceRecognition);
    
    // Crear botón para silenciar la voz
    const muteButton = document.createElement('button');
    muteButton.id = 'voice-mute-btn';
    muteButton.className = 'voice-btn';
    muteButton.setAttribute('aria-label', 'Silenciar asistente de voz');
    muteButton.innerHTML = '<i class="bi bi-volume-up"></i>';
    muteButton.title = 'Silenciar asistente de voz';
    
    // Añadir estilos del botón de silencio
    muteButton.style.position = 'fixed';
    muteButton.style.bottom = '90px';  // Colocar encima del botón de voz
    muteButton.style.right = '20px';   // Alinear con el botón de voz
    muteButton.style.width = '60px';
    muteButton.style.height = '60px';
    muteButton.style.borderRadius = '50%';
    muteButton.style.backgroundColor = '#28a745';
    muteButton.style.color = 'white';
    muteButton.style.border = 'none';
    muteButton.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
    muteButton.style.zIndex = '1000';
    muteButton.style.cursor = 'pointer';
    muteButton.style.fontSize = '1.5rem';  // Aumentar tamaño del ícono
    
    // Añadir el botón de silencio al DOM
    document.body.appendChild(muteButton);
    
    // Añadir manejador de eventos para el botón de silencio
    muteButton.addEventListener('click', toggleMute);
    
    // Inicializar el estado del botón de silencio basado en las preferencias guardadas
    updateMuteButtonState();
    
    // Crear elemento para mostrar texto del asistente
    const voiceOutput = document.createElement('div');
    voiceOutput.id = 'voice-output';
    voiceOutput.className = 'voice-output';
    voiceOutput.setAttribute('aria-live', 'polite');
    
    // Añadir estilos del elemento de salida
    voiceOutput.style.position = 'fixed';
    voiceOutput.style.bottom = '90px';
    voiceOutput.style.right = '20px';
    voiceOutput.style.maxWidth = '300px';
    voiceOutput.style.padding = '10px 15px';
    voiceOutput.style.backgroundColor = 'rgba(0,0,0,0.7)';
    voiceOutput.style.color = 'white';
    voiceOutput.style.borderRadius = '10px';
    voiceOutput.style.display = 'none';
    voiceOutput.style.zIndex = '999';
    
    // Añadir el elemento de salida al DOM
    document.body.appendChild(voiceOutput);
}

/**
 * Activa o desactiva el reconocimiento de voz
 */
function toggleVoiceRecognition() {
    if (!recognition) return;
    
    if (!isListening) {
        // Iniciar reconocimiento
        try {
            recognition.start();
            isListening = true;
            updateVoiceButtonState();
            showVoiceOutput('Te escucho...');
        } catch (error) {
            console.error('Error al iniciar el reconocimiento de voz:', error);
        }
    } else {
        // Detener reconocimiento
        try {
            recognition.stop();
            isListening = false;
            updateVoiceButtonState();
            hideVoiceOutput();
        } catch (error) {
            console.error('Error al detener el reconocimiento de voz:', error);
        }
    }
}

/**
 * Activa o desactiva el sonido del asistente de voz
 */
function toggleMute() {
    isMuted = !isMuted;
    // Guardar preferencia en localStorage
    localStorage.setItem('voiceAssistant_muted', isMuted);
    updateMuteButtonState();
    
    if (isMuted) {
        // Si hay algún mensaje hablando, detenerlo
        if (speechSynthesis.speaking) {
            speechSynthesis.cancel();
        }
        showVoiceOutput('Asistente de voz silenciado');
        setTimeout(() => {
            hideVoiceOutput();
        }, 2000);
    } else {
        showVoiceOutput('Asistente de voz activado');
        speakText('Asistente de voz activado. ¿En qué puedo ayudarte?');
        setTimeout(() => {
            hideVoiceOutput();
        }, 2000);
    }
}

/**
 * Actualiza el estado visual del botón de silencio
 */
function updateMuteButtonState() {
    const muteButton = document.getElementById('voice-mute-btn');
    if (!muteButton) return;
    
    if (isMuted) {
        muteButton.style.backgroundColor = '#dc3545';  // Rojo cuando está silenciado
        muteButton.innerHTML = '<i class="bi bi-volume-mute"></i>';
        muteButton.title = 'Activar asistente de voz';
    } else {
        muteButton.style.backgroundColor = '#28a745';  // Verde cuando está activo
        muteButton.innerHTML = '<i class="bi bi-volume-up"></i>';
        muteButton.title = 'Silenciar asistente de voz';
    }
}

/**
 * Actualiza el estado visual del botón del asistente
 */
function updateVoiceButtonState() {
    const voiceButton = document.getElementById('voice-assistant-btn');
    if (!voiceButton) return;
    
    if (isListening) {
        voiceButton.style.backgroundColor = '#dc3545';  // Rojo cuando está escuchando
        voiceButton.innerHTML = '<i class="bi bi-mic-fill"></i>';
        voiceButton.title = 'Asistente escuchando (Presiona para detener)';
    } else {
        voiceButton.style.backgroundColor = '#007bff';  // Azul cuando está inactivo
        voiceButton.innerHTML = '<i class="bi bi-mic"></i>';
        voiceButton.title = 'Asistente de voz (Presiona para hablar)';
    }
}

/**
 * Muestra un mensaje en el elemento de salida de voz
 * @param {string} text - El texto a mostrar
 */
function showVoiceOutput(text) {
    const voiceOutput = document.getElementById('voice-output');
    if (voiceOutput) {
        voiceOutput.textContent = text;
        voiceOutput.style.display = 'block';
    }
}

/**
 * Oculta el elemento de salida de voz
 */
function hideVoiceOutput() {
    const voiceOutput = document.getElementById('voice-output');
    if (voiceOutput) {
        voiceOutput.style.display = 'none';
    }
}

/**
 * Maneja los comandos de voz recibidos
 * @param {SpeechRecognitionEvent} event - El evento de reconocimiento
 */
function handleVoiceCommand(event) {
    const command = event.results[0][0].transcript.toLowerCase().trim();
    showVoiceOutput(`"${command}"`);
    
    // Procesar diferentes comandos
    if (command.includes('ir a') || command.includes('navegar a') || command.includes('abrir')) {
        navigateToPage(command);
    } else if (command.includes('describir') || command.includes('explica') || command.includes('qué es')) {
        describeCurrentPage();
    } else if (command.includes('buscar') || command.includes('encontrar')) {
        searchContent(command);
    } else if (command.includes('ayuda') || command.includes('asistente')) {
        provideHelp();
    } else if (command.includes('silenciar') || command.includes('silencio') || command.includes('mute')) {
        toggleMute();
    } else if (command.includes('activar voz') || command.includes('activar sonido') || command.includes('unmute')) {
        if (isMuted) {
            toggleMute();
        } else {
            speakText('El asistente de voz ya está activado.');
        }
    } else {
        speakText('No he podido entender el comando. Prueba a decir "ayuda" para ver los comandos disponibles.');
    }
}

/**
 * Navega a una página según el comando de voz
 * @param {string} command - El comando recibido
 */
function navigateToPage(command) {
    let targetPage = '';
    
    if (command.includes('inicio') || command.includes('home')) {
        targetPage = '/';
    } else if (command.includes('rutas')) {
        targetPage = '/rutas';
    } else if (command.includes('paradas')) {
        targetPage = '/paradas';
    } else if (command.includes('ayuda')) {
        targetPage = '/ayuda';
    } else if (command.includes('perfil')) {
        targetPage = '/auth/perfil';
    } else if (command.includes('administrador') || command.includes('admin')) {
        targetPage = '/admin';
    } else {
        speakText('No reconozco esa página. Puedo navegar a inicio, rutas, paradas, ayuda o perfil.');
        return;
    }
    
    speakText(`Navegando a ${targetPage.replace('/', '')}`);
    setTimeout(() => {
        window.location.href = targetPage;
    }, 1500);
}

/**
 * Describe la página actual
 */
function describeCurrentPage() {
    const currentPath = window.location.pathname;
    let description = '';
    
    if (currentPath === '/' || currentPath.endsWith('/index')) {
        description = pageDescriptions.inicio;
    } else if (currentPath.includes('/rutas')) {
        description = pageDescriptions.rutas;
    } else if (currentPath.includes('/paradas')) {
        description = pageDescriptions.paradas;
    } else if (currentPath.includes('/ayuda')) {
        description = pageDescriptions.ayuda;
    } else if (currentPath.includes('/perfil')) {
        description = pageDescriptions.perfil;
    } else if (currentPath.includes('/admin')) {
        description = pageDescriptions.admin;
    } else {
        description = 'No tengo información sobre esta página específica.';
    }
    
    speakText(description);
}

/**
 * Busca contenido según el comando
 * @param {string} command - El comando recibido
 */
function searchContent(command) {
    // Implementar según la funcionalidad de búsqueda disponible
    speakText('Lo siento, la función de búsqueda por voz aún no está disponible.');
}

/**
 * Proporciona ayuda sobre el uso del asistente
 */
function provideHelp() {
    const helpText = 'Puedo ayudarte a navegar por la aplicación. Algunos comandos disponibles son: "ir a rutas", "ir a paradas", "describir esta página", "ir a inicio", "silenciar", "activar voz", o "ir a ayuda".';
    speakText(helpText);
}

/**
 * Maneja errores de reconocimiento de voz
 * @param {SpeechRecognitionError} event - El evento de error
 */
function handleError(event) {
    console.error('Error en el reconocimiento de voz:', event.error);
    isListening = false;
    updateVoiceButtonState();
    
    let errorMessage;
    switch (event.error) {
        case 'no-speech':
            errorMessage = 'No he detectado ninguna palabra. Inténtalo de nuevo.';
            break;
        case 'not-allowed':
            errorMessage = 'El reconocimiento de voz no está permitido. Verifica los permisos del micrófono.';
            break;
        default:
            errorMessage = 'Ha ocurrido un error con el reconocimiento de voz.';
    }
    
    showVoiceOutput(errorMessage);
}

/**
 * Convierte texto a voz y lo reproduce
 * @param {string} text - El texto a convertir y reproducir
 */
function speakText(text) {
    // Mostrar el texto en la interfaz aunque esté silenciado
    showVoiceOutput(text);
    
    // Si está silenciado, solo mostrar el texto pero no reproducir audio
    if (isMuted) {
        return;
    }
    
    if (speechSynthesis) {
        // Detener cualquier voz en reproducción
        speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'es-ES';
        utterance.rate = 1.0;  // Velocidad normal
        utterance.pitch = 1.0; // Tono normal
        
        // Seleccionar una voz en español si está disponible
        const voices = speechSynthesis.getVoices();
        const spanishVoice = voices.find(voice => voice.lang.includes('es'));
        if (spanishVoice) {
            utterance.voice = spanishVoice;
        }
        
        // Reproducir la voz
        speechSynthesis.speak(utterance);
        
        // Ocultar el mensaje después de un tiempo proporcional a la longitud del texto
        // (aproximadamente tiempo para leer)
        const readingTimeMs = Math.min(Math.max(text.length * 90, 2000), 10000);
        setTimeout(() => {
            if (!isListening) {
                hideVoiceOutput();
            }
        }, readingTimeMs);
    }
}
