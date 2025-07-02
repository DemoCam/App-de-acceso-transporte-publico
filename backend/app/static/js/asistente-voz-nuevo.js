/**
 * Asistente de voz para la aplicación de transporte accesible
 * Permite interactuar con la aplicación mediante comandos de voz
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar variables para reconocimiento y síntesis de voz
    let recognition = null;
    const speechSynthesis = window.speechSynthesis;
    let isListening = false;
    
    // Configurar descripciones de páginas
    const pageDescriptions = {
        'inicio': 'Bienvenido a Transporte Accesible Cali, tu guía para moverte por la ciudad de manera inclusiva. Aquí puedes consultar rutas, paradas y recibir asistencia para planificar tu viaje.',
        'rutas': 'En esta sección puedes consultar todas las rutas disponibles del transporte público, ver sus frecuencias y horarios. Selecciona una ruta para ver su recorrido detallado.',
        'paradas': 'Aquí encuentras información sobre todas las paradas del sistema de transporte, incluyendo características de accesibilidad, ubicación y las rutas que pasan por cada parada.',
        'ayuda': 'En esta sección encontrarás guías de uso de la aplicación, consejos de accesibilidad y respuestas a preguntas frecuentes sobre el sistema de transporte.',
        'perfil': 'Esta es tu página de perfil personal donde puedes ver y actualizar tu información, revisar tu historial y personalizar tus preferencias.',
        'admin': 'Estás en el panel de administración donde puedes gestionar rutas, paradas, asociaciones entre rutas y paradas, y usuarios del sistema.'
    };
    
    // Verificar soporte para reconocimiento de voz
    if ('webkitSpeechRecognition' in window) {
        // Usar webkit para Chrome y derivados
        initRecognition(window.webkitSpeechRecognition);
        console.log("Reconocimiento de voz inicializado (webkit)");
    } else if ('SpeechRecognition' in window) {
        // Usar API estándar para otros navegadores compatibles
        initRecognition(window.SpeechRecognition);
        console.log("Reconocimiento de voz inicializado (estándar)");
    } else {
        // Mostrar mensaje de incompatibilidad
        console.warn("El reconocimiento de voz no está disponible en este navegador");
        showBrowserCompatWarning();
    }
    
    /**
     * Inicializa el reconocimiento de voz con el objeto apropiado
     * @param {object} RecognitionClass - La clase de reconocimiento a utilizar
     */
    function initRecognition(RecognitionClass) {
        recognition = new RecognitionClass();
        recognition.continuous = false;
        recognition.lang = 'es-ES';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        
        // Configurar eventos
        recognition.onresult = handleVoiceCommand;
        recognition.onerror = handleError;
        recognition.onend = () => {
            isListening = false;
            updateVoiceButtonState();
        };
        
        // Añadir botón y configurar interfaz
        setupVoiceAssistant();
        
        // Describir la página actual al cargar
        setTimeout(describeCurrentPage, 1500);
    }
    
    /**
     * Muestra una advertencia si el navegador no es compatible
     */
    function showBrowserCompatWarning() {
        setTimeout(() => {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-warning alert-dismissible fade show';
            alertDiv.setAttribute('role', 'alert');
            alertDiv.innerHTML = `
                <strong>¡Navegador no compatible!</strong> El reconocimiento de voz no está disponible en este navegador. 
                Intente con Google Chrome, Microsoft Edge o Safari para usar esta función.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
            `;
            
            const content = document.querySelector('.container') || document.querySelector('main') || document.body;
            if (content) {
                content.insertBefore(alertDiv, content.firstChild);
            }
        }, 1000);
    }
    
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
        if (!recognition) {
            showVoiceOutput('Lo siento, el reconocimiento de voz no está disponible en este navegador');
            return;
        }
        
        if (!isListening) {
            // Iniciar reconocimiento
            try {
                recognition.start();
                isListening = true;
                updateVoiceButtonState();
                showVoiceOutput('Te escucho...');
            } catch (error) {
                console.error('Error al iniciar el reconocimiento de voz:', error);
                showVoiceOutput('Error al iniciar el micrófono. Revisa los permisos.');
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
     * Muestra el texto de salida del asistente
     * @param {string} text - El texto a mostrar
     */
    function showVoiceOutput(text) {
        const voiceOutput = document.getElementById('voice-output');
        if (!voiceOutput) return;
        
        voiceOutput.textContent = text;
        voiceOutput.style.display = 'block';
        
        // Ocultar después de 5 segundos
        setTimeout(() => {
            if (voiceOutput.textContent === text) {
                hideVoiceOutput();
            }
        }, 5000);
    }
    
    /**
     * Oculta el texto de salida del asistente
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
        console.log("Comando de voz recibido:", command);
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
        let pageName = '';
        
        if (command.includes('inicio') || command.includes('home')) {
            targetPage = '/';
            pageName = 'inicio';
        } else if (command.includes('rutas')) {
            targetPage = '/rutas';
            pageName = 'rutas';
        } else if (command.includes('paradas')) {
            targetPage = '/paradas';
            pageName = 'paradas';
        } else if (command.includes('ayuda')) {
            targetPage = '/ayuda';
            pageName = 'ayuda';
        } else if (command.includes('perfil')) {
            targetPage = '/auth/perfil';
            pageName = 'perfil';
        } else if (command.includes('administrador') || command.includes('admin')) {
            targetPage = '/admin';
            pageName = 'administrador';
        } else {
            speakText('No reconozco esa página. Puedo navegar a inicio, rutas, paradas, ayuda o perfil.');
            return;
        }
        
        speakText(`Navegando a ${pageName}`);
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
        const helpText = 'Puedo ayudarte a navegar por la aplicación. Algunos comandos disponibles son: "ir a rutas", "ir a paradas", "describir esta página", "ir a inicio", "ir a perfil" o "ir a ayuda".';
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
        if (speechSynthesis) {
            // Detener cualquier voz en reproducción
            speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'es-ES';
            utterance.rate = 1.0;  // Velocidad normal
            utterance.pitch = 1.0; // Tono normal
            
            // Cargar voces disponibles
            let voices = speechSynthesis.getVoices();
            if (voices.length === 0) {
                // En algunos navegadores, las voces se cargan de forma asíncrona
                speechSynthesis.onvoiceschanged = function() {
                    voices = speechSynthesis.getVoices();
                    setSpanishVoice();
                };
            } else {
                setSpanishVoice();
            }
            
            function setSpanishVoice() {
                // Buscar una voz en español
                const spanishVoice = voices.find(voice => 
                    voice.lang.includes('es') || 
                    voice.name.includes('Spanish') || 
                    voice.name.includes('Español')
                );
                
                if (spanishVoice) {
                    utterance.voice = spanishVoice;
                    console.log("Usando voz:", spanishVoice.name);
                }
                
                // Mostrar el texto en la interfaz
                showVoiceOutput(text);
                
                // Reproducir la voz
                speechSynthesis.speak(utterance);
            }
        } else {
            console.warn('La síntesis de voz no es compatible con este navegador');
            showVoiceOutput(text);
        }
    }
});
