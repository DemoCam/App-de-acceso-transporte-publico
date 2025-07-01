/**
 * Asistente de voz para la App de Transporte Accesible Cali
 */

// Estado del asistente de voz
let vozActiva = false;
let reconocimientoVoz = null;
let sintetizadorVoz = window.speechSynthesis;

// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Elementos DOM
    const btnActivarVoz = document.getElementById('btnActivarVoz');
    
    // Inicializar el asistente de voz
    inicializarAsistenteVoz();
    
    // Verificar si hay soporte para síntesis de voz
    if (!sintetizadorVoz) {
        console.error('Tu navegador no soporta síntesis de voz');
    }
    
    // Verificar si hay soporte para reconocimiento de voz
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        console.error('Tu navegador no soporta reconocimiento de voz');
    }
    
    // Evento para botón de activar voz
    if (btnActivarVoz) {
        btnActivarVoz.addEventListener('click', function() {
            toggleVoz();
        });
    }
    
    // Recuperar estado guardado
    cargarEstadoVoz();
});

// Función para inicializar el asistente de voz
function inicializarAsistenteVoz() {
    // Configurar reconocimiento de voz si está disponible
    if ('webkitSpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        reconocimientoVoz = new SpeechRecognition();
        reconocimientoVoz.lang = 'es-ES';
        reconocimientoVoz.continuous = false;
        reconocimientoVoz.interimResults = false;
        reconocimientoVoz.maxAlternatives = 1;
        
        // Manejar resultados
        reconocimientoVoz.onresult = function(event) {
            const comando = event.results[0][0].transcript.trim().toLowerCase();
            console.log('Comando detectado:', comando);
            
            procesarComando(comando);
        };
        
        reconocimientoVoz.onerror = function(event) {
            console.error('Error en reconocimiento de voz:', event.error);
        };
        
        reconocimientoVoz.onend = function() {
            // Reiniciar si está activo
            if (vozActiva) {
                setTimeout(() => {
                    reconocimientoVoz.start();
                }, 1000);
            }
        };
    }
}

// Función para activar/desactivar el asistente de voz
function toggleVoz() {
    vozActiva = !vozActiva;
    
    // Actualizar botón
    const btnActivarVoz = document.getElementById('btnActivarVoz');
    if (btnActivarVoz) {
        if (vozActiva) {
            btnActivarVoz.classList.add('active');
            btnActivarVoz.innerText = 'Voz activa';
            btnActivarVoz.setAttribute('aria-pressed', 'true');
        } else {
            btnActivarVoz.classList.remove('active');
            btnActivarVoz.innerText = 'Activar voz';
            btnActivarVoz.setAttribute('aria-pressed', 'false');
        }
    }
    
    // Iniciar o detener reconocimiento
    if (vozActiva) {
        if (reconocimientoVoz) {
            try {
                reconocimientoVoz.start();
                anunciarMensaje('Asistente de voz activado. Dí "ayuda" para conocer los comandos disponibles.');
            } catch (e) {
                console.error('Error al iniciar el reconocimiento de voz:', e);
            }
        }
    } else {
        if (reconocimientoVoz) {
            try {
                reconocimientoVoz.stop();
                anunciarMensaje('Asistente de voz desactivado');
            } catch (e) {
                console.error('Error al detener el reconocimiento de voz:', e);
            }
        }
    }
    
    // Guardar estado
    localStorage.setItem('vozActiva', vozActiva ? 'true' : 'false');
}

// Función para anunciar mensajes por voz
function anunciarMensaje(mensaje) {
    if (!sintetizadorVoz) return;
    
    // Detener cualquier mensaje anterior
    sintetizadorVoz.cancel();
    
    const utterance = new SpeechSynthesisUtterance(mensaje);
    utterance.lang = 'es-ES';
    utterance.rate = 1.0; // Velocidad normal
    utterance.pitch = 1.0; // Tono normal
    utterance.volume = 1.0; // Volumen máximo
    
    sintetizadorVoz.speak(utterance);
}

// Función para procesar comandos de voz
function procesarComando(comando) {
    // Comandos de navegación
    if (comando.includes('ir a inicio')) {
        anunciarMensaje('Navegando a la página de inicio');
        window.location.href = '/';
        return;
    }
    
    if (comando.includes('buscar rutas') || comando.includes('consultar rutas')) {
        anunciarMensaje('Navegando a la página de consulta de rutas');
        window.location.href = '/rutas';
        return;
    }
    
    if (comando.includes('paradas cercanas')) {
        anunciarMensaje('Navegando a la página de paradas cercanas');
        window.location.href = '/paradas';
        return;
    }
    
    if (comando.includes('ayuda')) {
        anunciarMensaje('Navegando a la página de ayuda');
        window.location.href = '/ayuda';
        return;
    }
    
    // Comandos de búsqueda
    const buscarRutaMatch = comando.match(/buscar ruta (.*)/);
    if (buscarRutaMatch && buscarRutaMatch[1]) {
        const ruta = buscarRutaMatch[1].trim();
        if (window.location.pathname !== '/rutas') {
            anunciarMensaje(`Buscando ruta ${ruta}. Navegando a la página de rutas`);
            window.location.href = `/rutas?q=${encodeURIComponent(ruta)}`;
        } else {
            anunciarMensaje(`Buscando ruta ${ruta}`);
            document.getElementById('buscarRuta').value = ruta;
            document.getElementById('btnBuscarRuta').click();
        }
        return;
    }
    
    if (comando.includes('buscar paradas cercanas')) {
        if (window.location.pathname !== '/paradas') {
            anunciarMensaje('Para buscar paradas cercanas, primero navegaré a la página de paradas');
            window.location.href = '/paradas';
        } else {
            anunciarMensaje('Buscando paradas cercanas');
            document.getElementById('btnBuscarParadas').click();
        }
        return;
    }
    
    // Comandos de accesibilidad
    if (comando.includes('aumentar texto')) {
        anunciarMensaje('Aumentando el tamaño del texto');
        document.getElementById('btnAumentarTexto').click();
        return;
    }
    
    if (comando.includes('reducir texto')) {
        anunciarMensaje('Reduciendo el tamaño del texto');
        document.getElementById('btnReducirTexto').click();
        return;
    }
    
    if (comando.includes('alto contraste')) {
        anunciarMensaje('Cambiando el modo de contraste');
        document.getElementById('btnAltoContraste').click();
        return;
    }
    
    if (comando.includes('leer página')) {
        const contenidoPrincipal = document.getElementById('contenido-principal');
        if (contenidoPrincipal) {
            anunciarMensaje('Leyendo el contenido de la página: ' + contenidoPrincipal.textContent);
        } else {
            anunciarMensaje('No puedo encontrar el contenido principal para leer');
        }
        return;
    }
    
    // Si el comando no coincide con ninguno conocido
    anunciarMensaje('Comando no reconocido. Puedes decir "ayuda" para ver comandos disponibles');
}

// Cargar estado guardado
function cargarEstadoVoz() {
    const estadoGuardado = localStorage.getItem('vozActiva');
    if (estadoGuardado === 'true') {
        toggleVoz(); // Activa el asistente
    }
}

// Exportar funciones para uso global
window.anunciarMensaje = anunciarMensaje;
window.toggleVoz = toggleVoz;
