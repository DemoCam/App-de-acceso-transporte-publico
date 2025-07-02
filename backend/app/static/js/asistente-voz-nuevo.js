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
        'rutas': 'En esta sección puedes consultar todas las rutas disponibles del transporte público. Cada ruta muestra información como número, origen, destino, horarios y características de accesibilidad. Puedes buscar rutas usando el campo de búsqueda en la parte superior o filtrar por características como rampas para sillas de ruedas o anuncios de audio. Para conocer más detalles de una ruta, haz clic en su nombre para ver su trazado en el mapa, paradas asociadas y tiempo estimado de recorrido. Puedes usar comandos de voz como "buscar ruta" seguido del número o "filtrar rutas accesibles" para encontrar información más rápidamente.',
        'paradas': 'Aquí encuentras información sobre todas las paradas del sistema de transporte. Puedes ver la dirección exacta de cada parada, sus características de accesibilidad como rampas o semáforos sonoros, y consultar qué rutas pasan por ella. Utiliza el buscador para encontrar paradas por nombre o dirección, o filtra por características de accesibilidad usando los botones superiores. Para ver una parada en el mapa junto con las rutas que la conectan, haz clic en su nombre. Puedes usar comandos como "buscar parada" seguido del nombre o "mostrar paradas con rampa" para filtrar según tus necesidades.',
        'rutas_detalle': 'Estás viendo el detalle completo de una ruta. Aquí puedes observar el trazado exacto en el mapa, todas las paradas que forman parte del recorrido en orden secuencial, y los tiempos estimados entre cada punto. También se muestran las características de accesibilidad específicas de esta ruta, como disponibilidad de rampas, anuncios de audio y espacio para sillas de ruedas.',
        'paradas_detalle': 'Estás consultando los detalles de una parada específica. En esta página puedes ver la ubicación exacta en el mapa, la dirección completa, todas las rutas que pasan por esta parada con sus respectivos horarios, y las características de accesibilidad disponibles como rampas o semáforos sonoros.',
        'ayuda': 'En esta sección encontrarás guías de uso de la aplicación, consejos de accesibilidad y respuestas a preguntas frecuentes sobre el sistema de transporte.',
        'perfil': 'Esta es tu página de perfil personal donde puedes ver y actualizar tu información, revisar tu historial y personalizar tus preferencias.',
        'admin': 'Estás en el panel de administración donde puedes gestionar rutas, paradas, asociaciones entre rutas y paradas, y usuarios del sistema.',
        'asistente_voz': 'Estás en la guía del Asistente de Voz, una herramienta de accesibilidad que permite interactuar con la aplicación mediante comandos hablados. Aquí encontrarás instrucciones sobre cómo activar el asistente, los comandos disponibles para navegar por la aplicación, buscar rutas y paradas, y obtener información sobre el sistema de transporte. También puedes probar el asistente directamente desde esta página usando el botón de micrófono ubicado en la esquina inferior derecha de la pantalla.'
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
        
        // Configurar atajos de teclado y preferencias de accesibilidad
        setupKeyboardShortcuts();
        setupAccessibilityPreferences();
        
        // Crear un indicador visual para permitir la descripción automática
        const autoDescribeIndicator = document.createElement('div');
        autoDescribeIndicator.className = 'auto-describe-indicator';
        autoDescribeIndicator.innerHTML = `
            <div style="position: fixed; top: 70px; left: 50%; transform: translateX(-50%); 
                      background-color: rgba(0,0,0,0.7); color: white; padding: 10px 15px;
                      border-radius: 20px; z-index: 999; display: flex; align-items: center; 
                      cursor: pointer; box-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                <i class="bi bi-volume-up me-2"></i>
                <span>Describir esta página</span>
            </div>
        `;
        document.body.appendChild(autoDescribeIndicator);
        
        // Añadir evento de clic para describir la página
        autoDescribeIndicator.addEventListener('click', () => {
            describeCurrentPage();
            setTimeout(() => {
                autoDescribeIndicator.style.display = 'none';
            }, 500);
        });
        
        // Ocultar el indicador después de 10 segundos
        setTimeout(() => {
            autoDescribeIndicator.style.opacity = '0';
            autoDescribeIndicator.style.transition = 'opacity 1s ease';
            setTimeout(() => {
                autoDescribeIndicator.style.display = 'none';
            }, 1000);
        }, 10000);
        
        // Opcional: describir automáticamente la página para usuarios que tengan habilitada la opción
        if (typeof shouldAutoDescribePage === 'function' && shouldAutoDescribePage()) {
            setTimeout(describeCurrentPage, 1500);
        }
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
        voiceButton.style.bottom = '25px';
        voiceButton.style.right = '25px';
        voiceButton.style.width = '70px';
        voiceButton.style.height = '70px';
        voiceButton.style.borderRadius = '50%';
        voiceButton.style.backgroundColor = '#0056b3';
        voiceButton.style.color = 'white';
        voiceButton.style.border = 'none';
        voiceButton.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
        voiceButton.style.zIndex = '1000';
        voiceButton.style.cursor = 'pointer';
        voiceButton.style.fontSize = '24px';
        voiceButton.style.display = 'flex';
        voiceButton.style.alignItems = 'center';
        voiceButton.style.justifyContent = 'center';
        voiceButton.style.transition = 'all 0.3s ease';
        
        // Agregar efecto hover mediante un manejador de eventos
        voiceButton.addEventListener('mouseover', function() {
            this.style.transform = 'scale(1.1)';
            this.style.backgroundColor = '#0062cc';
        });
        
        voiceButton.addEventListener('mouseout', function() {
            this.style.transform = 'scale(1)';
            this.style.backgroundColor = isListening ? '#dc3545' : '#0056b3';
        });
        
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
        voiceOutput.style.bottom = '105px';
        voiceOutput.style.right = '25px';
        voiceOutput.style.maxWidth = '350px';
        voiceOutput.style.padding = '12px 18px';
        voiceOutput.style.backgroundColor = 'rgba(0,20,60,0.85)';
        voiceOutput.style.color = 'white';
        voiceOutput.style.borderRadius = '12px';
        voiceOutput.style.display = 'none';
        voiceOutput.style.zIndex = '999';
        voiceOutput.style.boxShadow = '0 4px 15px rgba(0,0,0,0.2)';
        voiceOutput.style.lineHeight = '1.5';
        voiceOutput.style.fontSize = '16px';
        
        // Añadir el elemento de salida al DOM
        document.body.appendChild(voiceOutput);
        
        // Mostrar un mensaje inicial para informar al usuario sobre el asistente
        setTimeout(() => {
            showVoiceOutput('Asistente de voz disponible. Haz clic en el botón azul y di "ayuda" para ver los comandos disponibles.');
        }, 2000);
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
        
        // Calcular tiempo basado en la longitud del texto
        // Aproximadamente 5 segundos + 50ms por carácter para textos largos
        const displayTime = Math.min(20000, 5000 + (text.length * 50));
        
        // Ocultar después del tiempo calculado
        setTimeout(() => {
            if (voiceOutput.textContent === text) {
                hideVoiceOutput();
            }
        }, displayTime);
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
        const commandRaw = event.results[0][0].transcript.trim();
        const command = commandRaw.toLowerCase();
        console.log("Comando de voz recibido:", commandRaw);
        showVoiceOutput(`"${commandRaw}"`);
        
        // Procesar diferentes comandos
        if (command.includes('ir a') || command.includes('navegar a') || command.includes('abrir')) {
            navigateToPage(command);
        } else if (command.includes('describir') || command.includes('explica') || command.includes('información') || 
                  command.includes('qué es') || command.includes('que hay') || command.includes('dónde estoy')) {
            describeCurrentPage();
        } else if (command.match(/buscar\s+((la\s+)?ruta|a|t|p|e)/i) || 
                  command.match(/encontrar\s+(ruta|a|t|p|e)/i) || 
                  command.match(/ruta\s+[a-z0-9]+/i)) {
            // Detectar patrones como "buscar ruta A15", "buscar A 15", "buscar T31", etc.
            searchRoute(commandRaw); // Usar el comando original para preservar mayúsculas
        } else if (command.match(/buscar\s+((la\s+)?parada)/i) || command.includes('encontrar parada')) {
            searchStop(commandRaw); // Usar el comando original para preservar mayúsculas
        } else if (command.includes('filtrar') || command.includes('mostrar solo') || command.includes('mostrar rutas') || command.includes('mostrar paradas')) {
            filterContent(command);
        } else if ((command.includes('ayuda') && !command.includes('ir a')) || command.includes('asistente') || command.includes('comandos disponibles')) {
            provideHelp();
        } else if (command.includes('volver') || command.includes('atrás') || command.includes('regresar')) {
            goBack();
        } else if (command.includes('inicio de página') || command.includes('subir') || command.includes('arriba')) {
            scrollToTop();
        } else if (command.includes('buscar') || command.includes('encontrar')) {
            searchContent(command);
        } else if (command.includes('leer')) {
            readCurrentContent(command);
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
        } else if (command.includes('asistente') || command.includes('voz') || command.includes('asistente de voz') || command.includes('guía de voz')) {
            targetPage = '/asistente_voz';
            pageName = 'asistente de voz';
        } else {
            speakText('No reconozco esa página. Puedo navegar a inicio, rutas, paradas, ayuda, perfil o asistente de voz.');
            return;
        }
        
        speakText(`Navegando a ${pageName}`);
        setTimeout(() => {
            window.location.href = targetPage;
        }, 1500);
    }
    
    /**
     * Describe la página actual con información detallada y contextual
     */
    function describeCurrentPage() {
        const currentPath = window.location.pathname;
        let description = '';
        
        if (currentPath === '/' || currentPath.endsWith('/index')) {
            description = pageDescriptions.inicio;
        } else if (currentPath.includes('/rutas/') && currentPath.split('/').length > 2) {
            // Estamos en detalle de una ruta específica
            description = pageDescriptions.rutas_detalle;
            // Añadir información específica de la ruta si está disponible
            const rutaNumero = document.querySelector('h1')?.textContent.match(/Ruta ([A-Z0-9]+)/)?.[1];
            if (rutaNumero) {
                const origenDestino = document.querySelector('.card-subtitle')?.textContent;
                description += ` Estás viendo la ruta ${rutaNumero}`;
                if (origenDestino) {
                    description += `, ${origenDestino}.`;
                }
            }
        } else if (currentPath.includes('/rutas')) {
            description = pageDescriptions.rutas;
            // Contar el número de rutas disponibles
            const numRutas = document.querySelectorAll('.ruta-item').length;
            if (numRutas > 0) {
                description += ` Hay ${numRutas} rutas disponibles en el sistema.`;
            }
            // Añadir información sobre cómo buscar
            description += ' Puedes decir "buscar ruta" seguido del número o nombre para encontrarla rápidamente.';
        } else if (currentPath.includes('/paradas/') && currentPath.split('/').length > 2) {
            // Estamos en detalle de una parada específica
            description = pageDescriptions.paradas_detalle;
            // Añadir información específica de la parada si está disponible
            const paradaNombre = document.querySelector('h1')?.textContent.match(/Parada: (.+)/)?.[1];
            if (paradaNombre) {
                description += ` Estás consultando la parada ${paradaNombre}.`;
                // Añadir características de accesibilidad si están disponibles
                const caracteristicas = [];
                if (document.querySelector('.badge-rampa')) {
                    caracteristicas.push('rampa para accesibilidad');
                }
                if (document.querySelector('.badge-semaforo')) {
                    caracteristicas.push('semáforo sonoro');
                }
                if (caracteristicas.length > 0) {
                    description += ` Esta parada cuenta con ${caracteristicas.join(' y ')}.`;
                }
            }
        } else if (currentPath.includes('/paradas')) {
            description = pageDescriptions.paradas;
            // Contar el número de paradas disponibles
            const numParadas = document.querySelectorAll('.parada-item').length;
            if (numParadas > 0) {
                description += ` Hay ${numParadas} paradas registradas en el sistema.`;
            }
            // Añadir información sobre cómo buscar
            description += ' Puedes decir "buscar parada" seguido del nombre o "filtrar paradas accesibles" para encontrar paradas con características de accesibilidad.';
        } else if (currentPath.includes('/ayuda')) {
            description = pageDescriptions.ayuda;
        } else if (currentPath.includes('/perfil')) {
            description = pageDescriptions.perfil;
        } else if (currentPath.includes('/admin')) {
            description = pageDescriptions.admin;
        } else if (currentPath.includes('/asistente_voz') || currentPath.includes('/asistente-voz')) {
            description = pageDescriptions.asistente_voz;
            // Añadir información adicional sobre las secciones disponibles en esta página
            const secciones = document.querySelectorAll('.list-group-item').length;
            if (secciones > 0) {
                description += ` La página está dividida en ${secciones} secciones que explican los diferentes aspectos del asistente. Puedes navegar entre ellas usando el menú lateral izquierdo.`;
            }
        } else {
            description = 'No tengo información detallada sobre esta página específica.';
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
     * Proporciona ayuda sobre el uso del asistente, adaptada al contexto
     */
    function provideHelp() {
        const currentPath = window.location.pathname;
        let helpText = 'Soy tu asistente de voz. Puedo ayudarte a navegar por la aplicación y encontrar la información que necesitas. ';
        
        // Comandos generales disponibles en todas las páginas
        const generalCommands = 'Los comandos generales incluyen: "ir a rutas", "ir a paradas", "ir a inicio", "describir esta página", "volver atrás" y "subir al inicio".';
        
        // Comandos específicos según la página actual
        if (currentPath.includes('/rutas/') && currentPath.split('/').length > 2) {
            // Estamos en detalle de una ruta específica
            helpText += 'En esta página de detalle de ruta, puedes usar comandos como: "leer mapa" para describir el trazado, "leer tabla" para escuchar las paradas en orden, o "volver a rutas" para regresar al listado. ';
        } else if (currentPath.includes('/rutas')) {
            // Estamos en el listado de rutas
            helpText += 'En la página de rutas, puedes decir: "buscar ruta" seguido del número o nombre, "filtrar rutas con rampa", "filtrar rutas con audio", "mostrar rutas con espacio para sillas", o "mostrar todas las rutas". También puedes decir "leer tabla" para escuchar las primeras rutas del listado. ';
        } else if (currentPath.includes('/paradas/') && currentPath.split('/').length > 2) {
            // Estamos en detalle de una parada específica
            helpText += 'En esta página de detalle de parada, puedes usar comandos como: "leer mapa" para describir la ubicación, "leer rutas" para escuchar las rutas que pasan por esta parada, o "volver a paradas" para regresar al listado. ';
        } else if (currentPath.includes('/paradas')) {
            // Estamos en el listado de paradas
            helpText += 'En la página de paradas, puedes decir: "buscar parada" seguido del nombre o dirección, "filtrar paradas con rampa", "mostrar paradas con semáforo sonoro", o "mostrar todas las paradas". También puedes decir "leer tabla" para escuchar las primeras paradas del listado. ';
        }
        
        // Añadir comandos generales al final
        helpText += generalCommands;
        
        // Añadir información sobre el asistente
        helpText += ' Para activarme nuevamente, solo haz clic en el botón redondo azul en la esquina inferior derecha de la pantalla.';
        
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
        // Mostrar el mensaje visualmente siempre
        showVoiceOutput(text);
        
        // Verificar si el asistente está silenciado usando la función global
        if (typeof isVoiceAssistantMuted === 'function' && isVoiceAssistantMuted()) {
            console.log('Asistente de voz silenciado. Mensaje:', text);
            return; // No reproducir voz si está silenciado
        }
        
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
    
    /**
     * Busca una ruta específica por número o nombre
     * @param {string} command - El comando recibido
     */
    function searchRoute(command) {
        // Extraer solo el identificador de la ruta del comando, eliminando todas las palabras clave
        let searchQuery = command;
        
        // Patrones para eliminar
        const patternesToRemove = [
            /\bbuscar\b/i, 
            /\bla\b/i, 
            /\bruta\b/i, 
            /\bencontrar\b/i, 
            /\bmostrar\b/i
        ];
        
        // Eliminar cada patrón
        patternesToRemove.forEach(pattern => {
            searchQuery = searchQuery.replace(pattern, '');
        });
        
        // Limpiar y normalizar
        searchQuery = searchQuery.trim();
        
        // MEJORA: Eliminar cualquier punto al final (problema común de reconocimiento de voz)
        // Aseguramos que esto funcione correctamente con una expresión más específica
        searchQuery = searchQuery.replace(/\.+$/, '');
        
        if (!searchQuery) {
            speakText('Por favor, indica el número o nombre de la ruta que quieres buscar.');
            return;
        }
        
        // MEJORA: Normalización más robusta para formatos de rutas
        // Normalizar espacios múltiples
        searchQuery = searchQuery.replace(/\s+/g, ' ');
        
        // Normalizar formatos comunes de rutas (A-15, A.15, A 15 -> A15)
        searchQuery = searchQuery.replace(/([A-Za-z])\s*[-\.]\s*(\d+)/gi, '$1$2'); 
        searchQuery = searchQuery.replace(/([A-Za-z])\s+(\d+)/gi, '$1$2');
        
        // Manejar casos especiales como "ruta A15" -> "A15"
        searchQuery = searchQuery.replace(/^ruta\s+([A-Za-z\d]+)$/i, '$1');
        
        console.log("Búsqueda de ruta normalizada:", searchQuery);
        
        // Verificar si estamos en la página de rutas
        if (!window.location.pathname.includes('/rutas')) {
            speakText(`Navegando a la sección de rutas para buscar: ${searchQuery}`);
            setTimeout(() => {
                window.location.href = `/rutas?q=${encodeURIComponent(searchQuery)}`;
            }, 1500);
            return;
        }
        
        // Si ya estamos en la página de rutas, realizar la búsqueda
        const searchInput = document.getElementById('buscar-ruta');
        if (searchInput) {
            // Establecer el valor de búsqueda normalizada
            searchInput.value = searchQuery;
            searchInput.focus();
            
            // Crear y enviar un evento personalizado para búsqueda inteligente
            const customEvent = new CustomEvent('smart-search', { 
                detail: { query: searchQuery, type: 'ruta' },
                bubbles: true 
            });
            searchInput.dispatchEvent(customEvent);
            
            // Como fallback, también activamos el comportamiento estándar de búsqueda
            const searchButton = document.getElementById('btn-buscar');
            if (searchButton) {
                searchButton.click();
                speakText(`Buscando la ruta: ${searchQuery}`);
            } else {
                // Simular el evento input para activar posibles event listeners
                const event = new Event('input', { bubbles: true });
                searchInput.dispatchEvent(event);
                speakText(`Mostrando resultados para la ruta: ${searchQuery}`);
            }
        } else {
            speakText('Lo siento, no puedo realizar la búsqueda en esta página.');
        }
    }
    
    /**
     * Busca una parada específica por nombre o dirección
     * @param {string} command - El comando recibido
     */
    function searchStop(command) {
        // Extraer el nombre de la parada del comando
        let searchQuery = command;
        
        // Patrones para eliminar
        const patternesToRemove = [
            /\bbuscar\b/i, 
            /\bla\b/i, 
            /\bparada\b/i, 
            /\bencontrar\b/i, 
            /\bmostrar\b/i
        ];
        
        // Eliminar cada patrón
        patternesToRemove.forEach(pattern => {
            searchQuery = searchQuery.replace(pattern, '');
        });
        
        // Limpiar y normalizar
        searchQuery = searchQuery.trim();
        
        // MEJORA: Eliminar cualquier punto al final (problema común de reconocimiento de voz)
        // Aseguramos que esto funcione correctamente con una expresión más específica
        searchQuery = searchQuery.replace(/\.+$/, '');
        
        if (!searchQuery) {
            speakText('Por favor, indica el nombre o dirección de la parada que quieres buscar.');
            return;
        }
        
        // MEJORA: Normalización más robusta para paradas
        // Normalizar espacios múltiples
        searchQuery = searchQuery.replace(/\s+/g, ' ').trim();
        
        // Manejar formatos de direcciones y nombres comunes en Cali
        searchQuery = searchQuery.replace(/(\d+)\s*[#°]\s*(\d+)/g, '$1 # $2'); // Normalizar formato de direcciones
        
        // Normalizar nombres de sectores o barrios comunes (usando strings para los patrones)
        const sectorPatterns = [
            { pattern: /\bsan\s+fernando\b/i, replacement: 'San Fernando' },
            { pattern: /\bel\s+poblado\b/i, replacement: 'El Poblado' },
            { pattern: /\bla\s+flora\b/i, replacement: 'La Flora' },
            { pattern: /\bciudad\s+jardin\b/i, replacement: 'Ciudad Jardín' }
            // Añadir más normalizaciones según sea necesario
        ];
        
        // Aplicar normalizaciones de sectores
        sectorPatterns.forEach(item => {
            searchQuery = searchQuery.replace(item.pattern, item.replacement);
        });
        
        console.log("Búsqueda de parada normalizada:", searchQuery);
        
        // Verificar si estamos en la página de paradas
        if (!window.location.pathname.includes('/paradas')) {
            speakText(`Navegando a la sección de paradas para buscar: ${searchQuery}`);
            setTimeout(() => {
                window.location.href = `/paradas?q=${encodeURIComponent(searchQuery)}`;
            }, 1500);
            return;
        }
        
        // Si ya estamos en la página de paradas, realizar la búsqueda
        const searchInput = document.getElementById('buscar-parada');
        if (searchInput) {
            searchInput.value = searchQuery;
            searchInput.focus();
            
            // Crear y enviar un evento personalizado para búsqueda inteligente
            const customEvent = new CustomEvent('smart-search', { 
                detail: { query: searchQuery, type: 'parada' },
                bubbles: true 
            });
            searchInput.dispatchEvent(customEvent);
            
            // Como fallback, también activamos el comportamiento estándar de búsqueda
            const searchButton = document.getElementById('btn-buscar');
            if (searchButton) {
                searchButton.click();
                speakText(`Buscando la parada: ${searchQuery}`);
            } else {
                // Simular el evento input para activar posibles event listeners
                const event = new Event('input', { bubbles: true });
                searchInput.dispatchEvent(event);
                speakText(`Mostrando resultados para la parada: ${searchQuery}`);
            }
        } else {
            speakText('Lo siento, no puedo realizar la búsqueda en esta página.');
        }
    }
    
    /**
     * Filtra contenido según criterios específicos
     * @param {string} command - El comando recibido
     */
    function filterContent(command) {
        // Determinar si estamos filtrando rutas o paradas
        const isRoutes = command.includes('rutas');
        const isStops = command.includes('paradas');
        
        // Determinar el tipo de filtro
        const filterByAccessibility = command.includes('accesible') || command.includes('con rampa') || 
                                     command.includes('con audio') || command.includes('espacio') || 
                                     command.includes('silla') || command.includes('semáforo');
                                     
        // Ir a la página correspondiente si no estamos en ella
        if (isRoutes && !window.location.pathname.includes('/rutas')) {
            speakText('Navegando a la sección de rutas para aplicar el filtro.');
            setTimeout(() => {
                window.location.href = '/rutas';
            }, 1500);
            return;
        } else if (isStops && !window.location.pathname.includes('/paradas')) {
            speakText('Navegando a la sección de paradas para aplicar el filtro.');
            setTimeout(() => {
                window.location.href = '/paradas';
            }, 1500);
            return;
        }
        
        // Aplicar filtros específicos
        if (isRoutes) {
            if (filterByAccessibility) {
                // Buscar botones de filtro para rutas accesibles
                const rampButton = document.querySelector('[data-filter="rampa"]') || document.querySelector('[data-filter-type="tiene_rampa"]');
                const audioButton = document.querySelector('[data-filter="audio"]') || document.querySelector('[data-filter-type="tiene_audio"]');
                const wheelchairButton = document.querySelector('[data-filter="silla"]') || document.querySelector('[data-filter-type="tiene_espacio_silla"]');
                
                if (command.includes('rampa') && rampButton) {
                    rampButton.click();
                    speakText('Mostrando rutas con rampa de acceso');
                } else if (command.includes('audio') && audioButton) {
                    audioButton.click();
                    speakText('Mostrando rutas con anuncios de audio');
                } else if ((command.includes('silla') || command.includes('espacio')) && wheelchairButton) {
                    wheelchairButton.click();
                    speakText('Mostrando rutas con espacio para sillas de ruedas');
                } else if (command.includes('todas') || command.includes('todos')) {
                    // Buscar botón para mostrar todas las rutas
                    const allButton = document.querySelector('[data-filter="all"]') || document.querySelector('.reset-filters');
                    if (allButton) {
                        allButton.click();
                        speakText('Mostrando todas las rutas disponibles');
                    }
                } else {
                    speakText('Para filtrar rutas puedes decir "mostrar rutas con rampa", "rutas con audio", o "rutas con espacio para sillas".');
                }
            } else {
                speakText('Para filtrar rutas puedes decir "mostrar rutas con rampa", "rutas con audio", o "rutas con espacio para sillas".');
            }
        } else if (isStops) {
            if (filterByAccessibility) {
                // Buscar botones de filtro para paradas accesibles
                const rampButton = document.querySelector('[data-filter="rampa"]') || document.querySelector('[data-filter-type="tiene_rampa"]');
                const trafficLightButton = document.querySelector('[data-filter="semaforo"]') || document.querySelector('[data-filter-type="tiene_semaforo_sonoro"]');
                
                if (command.includes('rampa') && rampButton) {
                    rampButton.click();
                    speakText('Mostrando paradas con rampa de acceso');
                } else if ((command.includes('semáforo') || command.includes('sonoro')) && trafficLightButton) {
                    trafficLightButton.click();
                    speakText('Mostrando paradas con semáforo sonoro');
                } else if (command.includes('todas') || command.includes('todos')) {
                    // Buscar botón para mostrar todas las paradas
                    const allButton = document.querySelector('[data-filter="all"]') || document.querySelector('.reset-filters');
                    if (allButton) {
                        allButton.click();
                        speakText('Mostrando todas las paradas disponibles');
                    }
                } else {
                    speakText('Para filtrar paradas puedes decir "mostrar paradas con rampa" o "paradas con semáforo sonoro".');
                }
            } else {
                speakText('Para filtrar paradas puedes decir "mostrar paradas con rampa" o "paradas con semáforo sonoro".');
            }
        } else {
            speakText('Puedes filtrar diciendo "mostrar rutas accesibles" o "mostrar paradas con rampa".');
        }
    }
    
    /**
     * Vuelve a la página anterior
     */
    function goBack() {
        speakText('Volviendo a la página anterior');
        setTimeout(() => {
            history.back();
        }, 1000);
    }
    
    /**
     * Desplaza la página al inicio
     */
    function scrollToTop() {
        speakText('Desplazándome al inicio de la página');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    /**
     * Lee el contenido principal de la página actual
     * @param {string} command - El comando recibido
     */
    function readCurrentContent(command) {
        // Intentar determinar qué contenido leer
        let contentToRead = '';
        const currentPath = window.location.pathname;
        
        if (command.includes('tabla') || command.includes('listado')) {
            // Leer información de tablas
            let tableContent = '';
            
            // MEJORA: Búsqueda exhaustiva de tablas y elementos tipo tabla en cualquier pestaña
            
            // 1. Intentar identificar tablas por selectores específicos según la pestaña actual
            let tableRows = [];
            let tableTitle = '';
            
            // Búsqueda específica por tipo de página (orden de prioridad)
            if (currentPath.includes('/rutas')) {
                tableRows = document.querySelectorAll('.ruta-item, .route-item, #lista-rutas .card, .tabla-rutas tr, .route-card');
                tableTitle = 'rutas';
            } else if (currentPath.includes('/paradas')) {
                tableRows = document.querySelectorAll('.parada-item, .stop-item, #tabla-paradas tr, #lista-paradas .card, .stop-card');
                tableTitle = 'paradas';
            } else if (currentPath.includes('/admin')) {
                tableRows = document.querySelectorAll('.admin-table tbody tr, .data-table tr');
                tableTitle = 'registros';
            }
            
            // 2. Si no se encontraron elementos específicos, buscar tablas HTML estándar
            if (tableRows.length === 0) {
                const htmlTables = document.querySelectorAll('table.table, table');
                
                if (htmlTables.length > 0) {
                    console.log("Encontradas tablas HTML:", htmlTables.length);
                    // Usar la primera tabla HTML como contenido tabular
                    const table = htmlTables[0];
                    const rows = table.querySelectorAll('tbody tr');
                    
                    if (rows.length > 0) {
                        // Intentar determinar un título para la tabla
                        const tableCaption = table.querySelector('caption')?.textContent.trim();
                        const nearbyHeader = table.closest('div, section')?.querySelector('h1, h2, h3, h4')?.textContent.trim();
                        tableTitle = tableCaption || nearbyHeader || 'datos';
                        
                        tableContent = `La tabla de ${tableTitle} muestra ${rows.length} filas de datos. `;
                        
                        // Obtener los encabezados para entender la estructura
                        const headers = Array.from(table.querySelectorAll('thead th, th')).map(th => th.textContent.trim());
                        
                        // Leer las primeras 5 filas como máximo
                        const maxRows = Math.min(rows.length, 5);
                        for (let i = 0; i < maxRows; i++) {
                            const cells = rows[i].querySelectorAll('td');
                            if (cells.length > 0) {
                                // Si hay encabezados, usarlos para dar contexto
                                if (headers.length >= cells.length) {
                                    tableContent += `Fila ${i+1}: `;
                                    for (let j = 0; j < Math.min(cells.length, 3); j++) {
                                        tableContent += `${headers[j]}: ${cells[j].textContent.trim()}. `;
                                    }
                                } else {
                                    // Si no hay encabezados, solo leer el contenido de las celdas
                                    tableContent += `Fila ${i+1}: ${cells[0].textContent.trim()}, ${cells.length > 1 ? cells[1].textContent.trim() : ''}. `;
                                }
                            }
                        }
                        
                        if (rows.length > 5) {
                            tableContent += 'Y otras filas más. ';
                        }
                    }
                } else {
                    // 3. Si no hay tablas, buscar estructuras tipo lista o cards
                    
                    // Intentar con diferentes selectores comunes para listas
                    const listSelectors = [
                        '.list-group-item',
                        '.card',
                        '.item',
                        'li.data-item',
                        '.list-item',
                        '.result-item',
                        'ul.results li',
                        '.collection-item',
                        '.data-row',
                        'div[role="listitem"]',
                        '.element-list > *'
                    ];
                    
                    // Buscar en cada selector hasta encontrar elementos
                    let listItems = [];
                    for (const selector of listSelectors) {
                        const items = document.querySelectorAll(selector);
                        if (items.length > 0) {
                            listItems = items;
                            break;
                        }
                    }
                    
                    if (listItems.length > 0) {
                        // Intentar determinar qué tipo de lista es
                        const containerElement = listItems[0].closest('div, section, ul');
                        const listHeader = containerElement?.querySelector('h1, h2, h3, h4')?.textContent.trim();
                        const sectionTitle = document.querySelector('h1, h2')?.textContent.trim();
                        tableTitle = listHeader || sectionTitle || 'elementos';
                        
                        tableContent = `Encontré una lista con ${listItems.length} ${tableTitle}. `;
                        
                        // Leer los primeros 5 elementos
                        const maxItems = Math.min(listItems.length, 5);
                        for (let i = 0; i < maxItems; i++) {
                            tableContent += `Elemento ${i+1}: ${listItems[i].textContent.trim().substring(0, 100).replace(/\s+/g, ' ')}. `;
                        }
                        
                        if (listItems.length > 5) {
                            tableContent += 'Y otros elementos más. ';
                        }
                    }
                }
            } else {
                // Procesar elementos específicos encontrados
                if (currentPath.includes('/rutas')) {
                    tableContent = `La tabla muestra ${tableRows.length} rutas. `;
                    // Leer las primeras 5 rutas como máximo
                    const maxRows = Math.min(tableRows.length, 5);
                    for (let i = 0; i < maxRows; i++) {
                        // Intentar diferentes selectores para adaptarse a diversas estructuras HTML
                        const routeNumber = tableRows[i].querySelector('.route-number, .numero-ruta, [data-route-id], .card-title')?.textContent.trim();
                        let routeName = tableRows[i].querySelector('.route-name, .nombre-ruta, .card-subtitle, .card-text')?.textContent.trim();
                        
                        // Si no se encontraron elementos específicos, usar el texto completo
                        if (!routeNumber && !routeName) {
                            tableContent += `Ruta ${i+1}: ${tableRows[i].textContent.trim().substring(0, 100).replace(/\s+/g, ' ')}. `;
                        } else {
                            // Si solo se encontró un valor, usarlo como número de ruta
                            if (routeNumber && !routeName) {
                                tableContent += `Ruta ${routeNumber}. `;
                            } else if (!routeNumber && routeName) {
                                tableContent += `Ruta: ${routeName}. `;
                            } else {
                                tableContent += `Ruta ${routeNumber}: ${routeName}. `;
                            }
                        }
                    }
                    if (tableRows.length > 5) {
                        tableContent += 'Y otras rutas más. ';
                    }
                } else if (currentPath.includes('/paradas')) {
                    tableContent = `La tabla muestra ${tableRows.length} paradas. `;
                    // Leer las primeras 5 paradas como máximo
                    const maxRows = Math.min(tableRows.length, 5);
                    for (let i = 0; i < maxRows; i++) {
                        const stopName = tableRows[i].querySelector('.stop-name, .nombre-parada, .card-title')?.textContent.trim();
                        const stopAddress = tableRows[i].querySelector('.stop-address, .direccion-parada, .card-text')?.textContent.trim();
                        
                        if (!stopName && !stopAddress) {
                            tableContent += `Parada ${i+1}: ${tableRows[i].textContent.trim().substring(0, 100).replace(/\s+/g, ' ')}. `;
                        } else if (stopName) {
                            tableContent += `Parada ${stopName}`;
                            if (stopAddress) {
                                tableContent += ` ubicada en ${stopAddress}`;
                            }
                            tableContent += '. ';
                        }
                    }
                    if (tableRows.length > 5) {
                        tableContent += 'Y otras paradas más. ';
                    }
                } else {
                    // Para otros tipos de tablas (administración, usuarios, etc.)
                    tableContent = `La tabla muestra ${tableRows.length} ${tableTitle || 'registros'}. `;
                    // Leer las primeras 5 filas como máximo
                    const maxRows = Math.min(tableRows.length, 5);
                    for (let i = 0; i < maxRows; i++) {
                        tableContent += `Registro ${i+1}: ${tableRows[i].textContent.trim().substring(0, 100).replace(/\s+/g, ' ')}. `;
                    }
                    if (tableRows.length > 5) {
                        tableContent += 'Y otros registros más. ';
                    }
                }
            }
            
            if (tableContent) {
                contentToRead = tableContent;
            } else {
                contentToRead = 'No encuentro información tabular para leer en esta página. Si estás seguro que hay una tabla, intenta con otro comando como "describir página".';
            }
        } else if (command.includes('mapa')) {
            // Describir mapa si existe
            const mapElement = document.getElementById('map') || document.getElementById('route-map') || document.querySelector('.leaflet-container');
            if (mapElement) {
                if (currentPath.includes('/rutas/')) {
                    const routeNumber = document.querySelector('h1')?.textContent.match(/Ruta ([A-Z0-9]+)/)?.[1];
                    contentToRead = `El mapa muestra el trazado completo de la ruta ${routeNumber || 'seleccionada'}, con todas las paradas marcadas en el recorrido.`;
                } else if (currentPath.includes('/paradas/')) {
                    const stopName = document.querySelector('h1')?.textContent.match(/Parada: (.+)/)?.[1];
                    contentToRead = `El mapa muestra la ubicación exacta de la parada ${stopName || 'seleccionada'} y las rutas que pasan por ella.`;
                } else {
                    contentToRead = 'El mapa muestra las ubicaciones de las paradas y rutas del sistema de transporte.';
                }
            } else {
                contentToRead = 'No encuentro un mapa en esta página para describir.';
            }
        } else if (command.includes('título') || command.includes('encabezado')) {
            // Leer el título de la página
            const pageTitle = document.querySelector('h1')?.textContent.trim();
            if (pageTitle) {
                contentToRead = `El título de la página es: ${pageTitle}`;
            } else {
                contentToRead = 'No encuentro un título principal en esta página.';
            }
        } else {
            // Leer información general de la página
            contentToRead = 'Para leer contenido específico, puedes decir "leer tabla", "leer mapa" o "leer título".';
        }
        
        speakText(contentToRead);
    }
    
    /**
     * Configura atajos de teclado para activar el asistente de voz
     */
    function setupKeyboardShortcuts() {
        document.addEventListener('keydown', function(event) {
            // Alt + A para activar/desactivar el asistente
            if (event.altKey && event.key === 'a') {
                event.preventDefault();
                toggleVoiceRecognition();
            }
            
            // Alt + H para obtener ayuda
            if (event.altKey && event.key === 'h') {
                event.preventDefault();
                provideHelp();
            }
            
            // Alt + D para describir la página actual
            if (event.altKey && event.key === 'd') {
                event.preventDefault();
                describeCurrentPage();
            }
        });
    }
    
    /**
     * Añade un panel de preferencias de accesibilidad
     */
    function setupAccessibilityPreferences() {
        // Crear botón de preferencias
        const prefsButton = document.createElement('button');
        prefsButton.className = 'a11y-prefs-button';
        prefsButton.setAttribute('aria-label', 'Preferencias de accesibilidad');
        prefsButton.innerHTML = '<i class="bi bi-gear"></i>';
        prefsButton.title = 'Preferencias de accesibilidad';
        
        // Estilos para el botón
        prefsButton.style.position = 'fixed';
        prefsButton.style.bottom = '25px';
        prefsButton.style.left = '25px';
        prefsButton.style.width = '50px';
        prefsButton.style.height = '50px';
        prefsButton.style.borderRadius = '50%';
        prefsButton.style.backgroundColor = '#6c757d';
        prefsButton.style.color = 'white';
        prefsButton.style.border = 'none';
        prefsButton.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
        prefsButton.style.zIndex = '1000';
        prefsButton.style.cursor = 'pointer';
        prefsButton.style.fontSize = '20px';
        prefsButton.style.display = 'flex';
        prefsButton.style.alignItems = 'center';
        prefsButton.style.justifyContent = 'center';
        
        document.body.appendChild(prefsButton);
        
        // Crear panel de preferencias
        const prefsPanel = document.createElement('div');
        prefsPanel.className = 'a11y-prefs-panel';
        prefsPanel.style.position = 'fixed';
        prefsPanel.style.bottom = '90px';
        prefsPanel.style.left = '25px';
        prefsPanel.style.width = '280px';
        prefsPanel.style.padding = '15px';
        prefsPanel.style.backgroundColor = 'white';
        prefsPanel.style.boxShadow = '0 0 15px rgba(0,0,0,0.2)';
        prefsPanel.style.borderRadius = '8px';
        prefsPanel.style.zIndex = '990';  // Z-index menor que el botón de micrófono (1000)
        prefsPanel.style.display = 'none';
        
        // Contenido del panel
        prefsPanel.innerHTML = `
            <h3 style="margin-top: 0; font-size: 18px;">Preferencias de Accesibilidad</h3>
            <div class="form-check form-switch my-3">
                <input class="form-check-input" type="checkbox" id="autoDescribePages">
                <label class="form-check-label" for="autoDescribePages">Describir páginas automáticamente</label>
            </div>
            <h4 style="font-size: 16px; margin-top: 15px;">Atajos de teclado:</h4>
            <ul style="padding-left: 20px;">
                <li>Alt + A: Activar asistente de voz</li>
                <li>Alt + H: Obtener ayuda</li>
                <li>Alt + D: Describir página actual</li>
            </ul>
            <button class="btn btn-sm btn-secondary mt-2" id="closePrefsBtn">Cerrar</button>
        `;
        
        document.body.appendChild(prefsPanel);
        
        // Cargar preferencia guardada
        const checkbox = prefsPanel.querySelector('#autoDescribePages');
        if (typeof shouldAutoDescribePage === 'function') {
            checkbox.checked = shouldAutoDescribePage();
        } else {
            // Fallback si la función global no está disponible
            checkbox.checked = localStorage.getItem('autoDescribePage') === 'true';
        }
        
        // Guardar preferencia al cambiar
        checkbox.addEventListener('change', function() {
            // Usar la función global si está disponible
            if (typeof saveAccessibilityPrefs === 'function') {
                saveAccessibilityPrefs(this.checked);
            } else {
                // Fallback por si no está disponible
                window.voiceAssistant = window.voiceAssistant || {};
                window.voiceAssistant.autoDescribe = this.checked;
                localStorage.setItem('autoDescribePage', this.checked);
            }
        });
        
        // Mostrar/ocultar panel
        prefsButton.addEventListener('click', function() {
            const isVisible = prefsPanel.style.display !== 'none';
            prefsPanel.style.display = isVisible ? 'none' : 'block';
        });
        
        // Botón cerrar
        prefsPanel.querySelector('#closePrefsBtn').addEventListener('click', function() {
            prefsPanel.style.display = 'none';
        });
    }
    
    /**
     * Actualiza el estado visual del botón de silencio interno
     */
    function updateMuteButtonState() {
        // Este código actualizaría el botón de silencio si existiera en la interfaz
        // Ahora usamos la función global updateMuteVisualState
        if (typeof updateMuteVisualState === 'function') {
            updateMuteVisualState();
        }
    }
    
    /**
     * Sistema de búsqueda inteligente que maneja coincidencias parciales y sugerencias
     * Esto mejora la experiencia de búsqueda del usuario cuando los comandos de voz
     * no son reconocidos perfectamente
     */
    document.addEventListener('smart-search', function(e) {
        // Extraer datos del evento
        const query = e.detail.query;
        const type = e.detail.type; // 'ruta' o 'parada'
        
        if (!query) return;
        
        console.log(`Sistema de búsqueda inteligente activado para ${type}: "${query}"`);
        
        // Identificar el contenedor de resultados según el tipo
        let itemSelector, containerSelector;
        
        if (type === 'ruta') {
            itemSelector = '.ruta-item'; // Ajustar según la estructura HTML real
            containerSelector = '#lista-rutas'; // Ajustar según la estructura HTML real
        } else if (type === 'parada') {
            itemSelector = '.parada-item'; // Ajustar según la estructura HTML real
            containerSelector = '#lista-paradas'; // Ajustar según la estructura HTML real
        } else {
            return; // Tipo no reconocido
        }
        
        // Función para puntuar la similitud de una cadena con la consulta
        function getSimilarityScore(text, query) {
            if (!text || !query) return 0;
            
            text = text.toLowerCase();
            query = query.toLowerCase();
            
            // Coincidencia exacta
            if (text.includes(query)) return 1.0;
            
            // Si la consulta es una letra seguida de números (ej: "A15")
            if (/^[a-z]\d+$/.test(query)) {
                const letter = query.charAt(0);
                const number = query.substring(1);
                
                // Buscar patrones como "A 15", "A-15", "A.15", etc.
                if (text.includes(`${letter} ${number}`) || 
                    text.includes(`${letter}-${number}`) ||
                    text.includes(`${letter}.${number}`)) {
                    return 0.9;
                }
                
                // Si contiene la letra sola
                if (text.includes(` ${letter} `)) return 0.3;
                
                // Si contiene el número solo
                if (text.includes(` ${number} `)) return 0.2;
            }
            
            // Para búsquedas de texto más generales
            let matchCount = 0;
            const words = query.split(/\s+/);
            
            words.forEach(word => {
                if (text.includes(word)) matchCount++;
            });
            
            // Calcular un puntaje basado en cuántas palabras coinciden
            return words.length > 0 ? matchCount / words.length * 0.7 : 0;
        }
        
        // Buscar todos los elementos y calcular su puntuación de similitud
        setTimeout(() => {
            const container = document.querySelector(containerSelector);
            if (!container) return;
            
            const items = container.querySelectorAll(itemSelector);
            if (!items || items.length === 0) return;
            
            let visibleCount = 0;
            let hasExactMatch = false;
            
            // Analizar cada elemento y calcular su puntaje
            items.forEach(item => {
                const text = item.textContent;
                const score = getSimilarityScore(text, query);
                
                // Elementos con puntaje alto se consideran coincidencias
                if (score >= 0.8) {
                    item.style.display = '';
                    visibleCount++;
                    hasExactMatch = true;
                    
                    // Destacar la coincidencia
                    item.style.backgroundColor = 'rgba(255, 255, 0, 0.2)';
                    setTimeout(() => {
                        item.style.backgroundColor = '';
                    }, 3000);
                } 
                // Si no hay coincidencias exactas, mostrar sugerencias parciales
                else if (!hasExactMatch && score >= 0.2) {
                    item.style.display = '';
                    visibleCount++;
                }
            });
            
            // Mensaje para el usuario cuando hay resultados similares
            if (visibleCount > 0 && !hasExactMatch) {
                speakText(`No encontré coincidencias exactas para ${query}, pero te muestro ${visibleCount} resultados similares.`);
            } 
            // Mensaje cuando no hay resultados
            else if (visibleCount === 0) {
                speakText(`No encontré coincidencias para ${query}. Intenta con otra búsqueda.`);
                
                // Mostrar todas las opciones como ayuda
                items.forEach(item => {
                    item.style.display = '';
                });
            }
        }, 500); // Pequeño retardo para asegurar que la búsqueda estándar también se procese
    });
});
