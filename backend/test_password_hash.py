"""
Script para probar la generación y verificación de hashes de contraseñas
"""
from werkzeug.security import generate_password_hash, check_password_hash
import sys

def test_password_hash():
    """Prueba la generación y verificación de hashes de contraseñas"""
    password = "Admin2025!"
    
    # Generar hash con diferentes métodos
    hash_pbkdf2 = generate_password_hash(password, method='pbkdf2:sha256')
    hash_sha256 = generate_password_hash(password, method='pbkdf2:sha256:50000')
    hash_scrypt = generate_password_hash(password, method='scrypt')
    
    print("\n1. Hash generados:")
    print(f"pbkdf2:sha256: {hash_pbkdf2}")
    print(f"pbkdf2:sha256:50000: {hash_sha256}")
    print(f"scrypt: {hash_scrypt}")
    
    print("\n2. Verificación de contraseñas:")
    print(f"pbkdf2:sha256 - Correcta: {check_password_hash(hash_pbkdf2, password)}")
    print(f"pbkdf2:sha256 - Incorrecta: {check_password_hash(hash_pbkdf2, 'ContraseñaIncorrecta')}")
    print(f"pbkdf2:sha256:50000 - Correcta: {check_password_hash(hash_sha256, password)}")
    print(f"pbkdf2:sha256:50000 - Incorrecta: {check_password_hash(hash_sha256, 'ContraseñaIncorrecta')}")
    print(f"scrypt - Correcta: {check_password_hash(hash_scrypt, password)}")
    print(f"scrypt - Incorrecta: {check_password_hash(hash_scrypt, 'ContraseñaIncorrecta')}")
    
    # Prueba manual para verificar un hash específico
    if len(sys.argv) > 1:
        test_hash = sys.argv[1]
        print(f"\n3. Verificación manual del hash proporcionado:")
        print(f"Hash: {test_hash}")
        print(f"¿Coincide con 'Admin2025!'? {check_password_hash(test_hash, 'Admin2025!')}")
        print(f"¿Coincide con 'admin123'? {check_password_hash(test_hash, 'admin123')}")

if __name__ == "__main__":
    test_password_hash()
