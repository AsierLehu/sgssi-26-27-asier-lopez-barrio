# Laboratorio: Cifrado simétrico

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Herramientas necesarias: OpenSSL (`sudo apt install openssl`).
- Repositorio GitHub de asignatura: puedes subir los programa desarrollados en el laboratorio.

## Ataque fuerza bruta al cifrado César

Crea un programa, en el lenguaje que quieras, que realice un ataque de fuerza bruta contra el siguiente mensaje: "Uunejvxb dw vdwmx wdnex jzdr, nw wdnbcaxb lxajixwnb". Es decir, el programa tiene que inferir la clave y usarla para descifrar el mensaje (PISTA: detección de idioma en Python). 

## Ataque fuerza bruta al cifrado simple por sustitución

Crea un programa, en el lenguaje que quieras, que realice un ataque de fuerza bruta contra el siguiente mensaje:

RIJ AZKKZHC PIKCE XT ACKCUXJHX SZX, E NZ PEJXKE, PXGIK XFDKXNEQE RIPI RIPQEHCK ET OENRCNPI AXNAX ZJ RKCHXKCI AX CJAXDXJAXJRCE AX RTENX, E ACOXKXJRCE AXT RITEQIKERCIJCNPI OKXJHXDIDZTCNHE AX TE ACKXRRCIJ EJEKSZCNHE.

AZKKZHC OZX ZJ OERHIK AX DKCPXK IKAXJ XJ XT DEDXT AX TE RTENX IQKXKE XJ REHETZJVE XJ GZTCI AX 1936. DXKI AZKKZHC, RIPI IRZKKX RIJ TEN DXKNIJETCAEAXN XJ TE MCNHIKCE, JI REVI AXT RCXTI. DXKNIJCOCREQE TE HKEACRCIJ KXvITZRCIJEKCE AX TE RTENX IQKXKE. NZ XJIKPX DIDZTEKCAEA XJHKX TE RTENX HKEQEGEAIKE, KXOTXGEAE XJ XT XJHCXKKI PZTHCHZACJEKCI XJ QEKRXTIJE XT 22 AX JIvCXPQKX AX 1936, PZXNHKE XNE CAXJHCOCRERCIJ. NZ PZXKHX OZX NCJ AZAE ZJ UITDX IQGXHCvI ET DKIRXNI KXvITZRCIJEKCI XJ PEKRME. NCJ AZKKZHC SZXAI PEN TCQKX XT REPCJI DEKE SZX XT XNHETCJCNPI, RIJ TE RIPDTCRCAEA AXT UIQCXKJI AXT OKXJHX DIDZTEK V AX TE ACKXRRCIJ EJEKSZCNHE, HXKPCJEKE XJ PEVI AX 1937 TE HEKXE AX TCSZCAEK TE KXvITZRCIJ, AXNPIKETCLEJAI E TE RTENX IQKXKE V OERCTCHEJAI RIJ XTTI XT DINHXKCIK HKCZJOI OKEJSZCNHE.

El mensaje está en castellano y deberás usar el análisis de frecuencias mediante la siguiente tabla:

![Frecuencias](Fecuencias.png)

(PISTA: el programa puede ser interactivo).

## Cifrado de flujo mediante XOR

Implementa un programa que cifre y descifre mensajes mediante un cifrado de flujo sencillo. El programa debe:

- Leer un mensaje y una clave de la misma longitud, representados como cadenas de bytes.
- Aplicar la operación XOR byte a byte entre el mensaje y la clave para obtener el criptograma.
- Usar la misma operación XOR para recuperar el mensaje original a partir del criptograma.
- Mostrar el mensaje original, la clave y el criptograma en hexadecimal.
- Comprobar que el descifrado del criptograma produce exactamente el mensaje original.

Utiliza los siguientes datos de prueba:

- Mensaje: `ATAQUE AL AMANECER`
- Clave: `CLAVE12345678901`

## Cifrado y descifrado con OpenSSL

Utiliza la herramienta `openssl enc` desde un terminal de Ubuntu para cifrar y descifrar un archivo con AES, Triple DES y DES. No tienes que implementar ningún programa.

Prepara un mensaje y una contraseña en archivos separados:

```bash
printf '%s\n' 'La criptografia protege la confidencialidad de la informacion.' > mensaje.txt
printf '%s\n' 'Laboratorio2026' > clave.txt
```

Cifra y descifra el mensaje con AES-256-CBC:

```bash
openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -salt \
	-in mensaje.txt -out mensaje.aes -pass file:clave.txt
openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 \
	-in mensaje.aes -out mensaje.aes.descifrado -pass file:clave.txt
cmp mensaje.txt mensaje.aes.descifrado
```

cat mensaje.aes.descifrado 
La criptografia protege la confidencialidad de la informacion.


### Explicación comandos OpenSSL

**Comando 1: Cifrado**
```bash
openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -salt \
	-in mensaje.txt -out mensaje.aes -pass file:clave.txt
```
- `openssl enc`: Herramienta de cifrado/descifrado de OpenSSL
- `-aes-256-cbc`: Algoritmo AES con clave de 256 bits en modo CBC (Cipher Block Chaining)
- `-pbkdf2`: Función de derivación de clave basada en contraseña (Password-Based Key Derivation Function 2)
- `-iter 100000`: Número de iteraciones para PBKDF2 (aumenta la seguridad contra ataques de fuerza bruta)
- `-salt`: Añade sal aleatoria para evitar ataques de diccionario
- `-in mensaje.txt`: Archivo de entrada (texto plano)
- `-out mensaje.aes`: Archivo de salida (texto cifrado)
- `-pass file:clave.txt`: Obtiene la contraseña desde el archivo `clave.txt`

**Comando 2: Descifrado**
```bash
openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 \
	-in mensaje.aes -out mensaje.aes.descifrado -pass file:clave.txt
```

- `-d`: Modo descifrado (decrypt)
- Los demás parámetros deben coincidir exactamente con los del cifrado
- `-in mensaje.aes`: Archivo cifrado de entrada
- `-out mensaje.aes.descifrado`: Archivo descifrado de salida

**Comando 3: Verificación**
```bash
cmp mensaje.txt mensaje.aes.descifrado
```

- `cmp`: Compara byte a byte dos archivos
- Si no produce salida, los archivos son idénticos (descifrado exitoso)


----------------------------------------

Repite la práctica con Triple DES y DES:

```bash
openssl enc -des-ede3-cbc -provider default -provider legacy -pbkdf2 \
	-iter 100000 -salt -in mensaje.txt -out mensaje.3des \
	-pass file:clave.txt
openssl enc -d -des-ede3-cbc -provider default -provider legacy -pbkdf2 \
	-iter 100000 -in mensaje.3des -out mensaje.3des.descifrado \
	-pass file:clave.txt
cmp mensaje.txt mensaje.3des.descifrado

openssl enc -des-cbc -provider default -provider legacy -pbkdf2 \
	-iter 100000 -salt -in mensaje.txt -out mensaje.des \
	-pass file:clave.txt
openssl enc -d -des-cbc -provider default -provider legacy -pbkdf2 \
	-iter 100000 -in mensaje.des -out mensaje.des.descifrado \
	-pass file:clave.txt
cmp mensaje.txt mensaje.des.descifrado
```

### Diferencias respecto a AES-256-CBC
1. **Algoritmo de cifrado:**
   - **AES anterior**: `-aes-256-cbc` (AES con clave de 256 bits)
   - **3DES**: `-des-ede3-cbc` (Triple DES con clave efectiva de 168 bits)
   - **DES**: `-des-cbc` (DES simple con clave de 56 bits)

2. **Proveedores requeridos:**
   - **Nuevo**: `-provider default -provider legacy`
   - **Razón**: DES y 3DES son algoritmos legacy (obsoletos) que requieren el proveedor legacy de OpenSSL 3.
3. **Nivel de seguridad:**
   - **AES-256**: Muy alta seguridad (estándar actual)
   - **3DES**: Seguridad media (en desuso gradual)
   - **DES**: Seguridad baja (considerado inseguro)
4. **Tamaño de bloque:**
   - **AES**: 128 bits por bloque
   - **DES/3DES**: 64 bits por bloque (menor eficiencia)
```

Compara el tamaño de los criptogramas y verifica su integridad mediante sus sumas SHA-256:

```bash
sha256sum mensaje.txt mensaje.aes mensaje.3des mensaje.des
sha256sum mensaje.aes.descifrado mensaje.3des.descifrado mensaje.des.descifrado
```

**Explicación `sha256sum`:** Estos comandos calculan el hash SHA-256 de los archivos para verificar integridad. El primer comando muestra los hashes del archivo original y los cifrados . El segundo muestra los hashes de los descifrados, que son idénticos al original si todo ha salido bien.

¿Que quiere decir CBC en -des-ede3-cbc?¿Hay otras opciones?

Cipher Block Chaining (Encadenamiento de Bloques). Es un modo de operación que encadena cada bloque con el anterior usando XOR y un vector de inicialización aleatorio.




