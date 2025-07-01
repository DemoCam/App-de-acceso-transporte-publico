/**
 * Funciones de accesibilidad para la App de Transporte Accesible Cali
 */

// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Elementos DOM
    const btnAumentarTexto = document.getElementById('btnAumentarTexto');
    const btnReducirTexto = document.getElementById('btnReducirTexto');
    const btnAltoContraste = document.getElementById('btnAltoContraste');
    const alertAccesibilidad = document.getElementById('alertAccesibilidad');
    
    // Variables para el tamaño de texto
    let tamañoTextoActual = 0; // 0 = normal, 1 = grande, 2 = extra grande
    
    // Recuperar preferencias guardadas
    cargarPreferencias();
    
    // Eventos para botones de accesibilidad
    if (btnAumentarTexto) {
        btnAumentarTexto.addEventListener('click', function() {
            aumentarTamaño();
        });
    }
    
    if (btnReducirTexto) {
        btnReducirTexto.addEventListener('click', function() {
            reducirTamaño();
        });
    }
    
    if (btnAltoContraste) {
        btnAltoContraste.addEventListener('click', function() {
            toggleAltoContraste();
        });
    }
    
    // Evento para cerrar la alerta de accesibilidad y recordar preferencia
    if (alertAccesibilidad) {
        const btnCerrarAlerta = alertAccesibilidad.querySelector('.btn-close');
        if (btnCerrarAlerta) {
            btnCerrarAlerta.addEventListener('click', function() {
                localStorage.setItem('alertaAccesibilidadCerrada', 'true');
            });
        }
        
        // Ocultar alerta si ya se cerró antes
        if (localStorage.getItem('alertaAccesibilidadCerrada') === 'true') {
            alertAccesibilidad.style.display = 'none';
        }
    }
    
    // Activar accesibilidad con teclas
    document.addEventListener('keydown', function(e) {
        // Alt + V para activar asistente de voz
        if (e.altKey && e.key === 'v') {
            e.preventDefault();
            toggleAsistenteVoz();
        }
        
        // Alt + C para alto contraste
        if (e.altKey && e.key === 'c') {
            e.preventDefault();
            toggleAltoContraste();
        }
        
        // Alt + + para aumentar texto
        if (e.altKey && e.key === '+') {
            e.preventDefault();
            aumentarTamaño();
        }
        
        // Alt + - para reducir texto
        if (e.altKey && e.key === '-') {
            e.preventDefault();
            reducirTamaño();
        }
    });
    
    // Funciones de accesibilidad
    
    // Función para aumentar el tamaño del texto
    function aumentarTamaño() {
        if (tamañoTextoActual < 2) {
            tamañoTextoActual++;
            aplicarTamañoTexto();
            guardarPreferencias();
            
            // Anunciar cambio si el asistente de voz está activo
            if (typeof anunciarMensaje === 'function') {
                const mensajes = [
                    'Tamaño de texto aumentado a grande',
                    'Tamaño de texto aumentado a muy grande'
                ];
                anunciarMensaje(mensajes[tamañoTextoActual - 1]);
            }
        } else {
            if (typeof anunciarMensaje === 'function') {
                anunciarMensaje('Ya estás en el tamaño de texto máximo');
            }
        }
    }
    
    // Función para reducir el tamaño del texto
    function reducirTamaño() {
        if (tamañoTextoActual > 0) {
            tamañoTextoActual--;
            aplicarTamañoTexto();
            guardarPreferencias();
            
            // Anunciar cambio
            if (typeof anunciarMensaje === 'function') {
                const mensajes = [
                    'Tamaño de texto vuelto a normal',
                    'Tamaño de texto reducido a grande'
                ];
                anunciarMensaje(mensajes[tamañoTextoActual]);
            }
        } else {
            if (typeof anunciarMensaje === 'function') {
                anunciarMensaje('Ya estás en el tamaño de texto mínimo');
            }
        }
    }
    
    // Aplicar el tamaño de texto adecuado
    function aplicarTamañoTexto() {
        document.body.classList.remove('text-large', 'text-xl');
        
        if (tamañoTextoActual === 1) {
            document.body.classList.add('text-large');
        } else if (tamañoTextoActual === 2) {
            document.body.classList.add('text-xl');
        }
    }
    
    // Alternar modo de alto contraste
    function toggleAltoContraste() {
        const altoContrasteActivo = document.body.classList.toggle('high-contrast');
        
        // Guardar preferencia
        localStorage.setItem('altoContraste', altoContrasteActivo ? 'true' : 'false');
        
        // Anunciar cambio
        if (typeof anunciarMensaje === 'function') {
            const mensaje = altoContrasteActivo ? 
                'Modo de alto contraste activado' : 
                'Modo de alto contraste desactivado';
            anunciarMensaje(mensaje);
        }
    }
    
    // Función para activar/desactivar asistente de voz
    // La implementación real estará en asistente-voz.js
    function toggleAsistenteVoz() {
        if (typeof toggleVoz === 'function') {
            toggleVoz();
        } else {
            console.warn('El asistente de voz no está disponible');
        }
    }
    
    // Guardar preferencias en localStorage
    function guardarPreferencias() {
        localStorage.setItem('tamañoTexto', tamañoTextoActual.toString());
    }
    
    // Cargar preferencias del usuario
    function cargarPreferencias() {
        // Cargar tamaño de texto
        const tamañoGuardado = localStorage.getItem('tamañoTexto');
        if (tamañoGuardado !== null) {
            tamañoTextoActual = parseInt(tamañoGuardado, 10);
            aplicarTamañoTexto();
        }
        
        // Cargar preferencia de alto contraste
        const contrasteGuardado = localStorage.getItem('altoContraste');
        if (contrasteGuardado === 'true') {
            document.body.classList.add('high-contrast');
        }
    }
});
