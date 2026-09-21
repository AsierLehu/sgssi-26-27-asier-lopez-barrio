message = "ATAQUEALAMANECER"
key = "CLAVE12345678901"  



def cifrar_xor(mensaje_bytes, clave_bytes):    
    # Aplicar XOR byte a byte
    resultado = []
    for i in range(len(mensaje_bytes)):
        byte_xor = mensaje_bytes[i] ^ clave_bytes[i] # ^ es operador lógico de XOR
        resultado.append(byte_xor)
    
    return bytes(resultado)

def bytes_a_hex(datos):
    return datos.hex().upper() # a hexadecimal y en mayusculas


def main(mensaje, clave):    
    
    print(f"Mensaje original: '{mensaje}'")
    print(f"Clave utilizada: '{clave}'")
    
        # Convertir strings a bytes
    mensaje_bytes = mensaje.encode('utf-8') # de texto a bytes
    clave_bytes = clave.encode('utf-8')
        
    # Cifrar el mensaje
    criptograma = cifrar_xor(mensaje_bytes, clave_bytes)

    mensaje_descifrado_bytes = cifrar_xor(criptograma, clave_bytes)
    mensaje_descifrado = mensaje_descifrado_bytes.decode('utf-8')

    print(f"Mensaje original / mensaje descifrado(hex): {bytes_a_hex(mensaje_descifrado_bytes)}")
    print(f"Clave (hex):      {bytes_a_hex(clave_bytes)}")
    print(f"Criptograma (hex): {bytes_a_hex(criptograma)}")

    print(f"Mensaje descifrado: '{mensaje_descifrado}'")
    
 

if __name__ == "__main__":
    main(message, key)