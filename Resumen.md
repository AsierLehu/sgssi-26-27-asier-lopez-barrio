# Resumen de laboratorios — SGSSI

## Al llegar al ordenador de la práctica

```bash
ssh-keygen -t ed25519 -C "email@ikasle.ehu.eus"   # genera el par en ~/.ssh/id_ed25519 o sino moverlo esa carpeta
eval "$(ssh-agent -s)"                                  # arranca el agente en segundo plano
ssh-add ~/.ssh/id_ed25519                               # carga la clave privada en el agente
cat ~/.ssh/id_ed25519.pub                               # muestra la pública para copiarla
```
La pública se pega en Google Cloud, en las claves SSH de la cuenta.
```bash
ssh alopez572@IP_EXTERNA
```

---

Índice:

1. [Introducción al cifrado, esteganografía y hashes](#1-introducción-al-cifrado-esteganografía-y-hashes)
2. [Docker](#2-docker)
3. [Cifrado simétrico](#3-cifrado-simétrico)
4. [Cifrado asimétrico](#4-cifrado-asimétrico)
5. [Aplicaciones del cifrado](#5-aplicaciones-del-cifrado)

---

## 1. Introducción al cifrado, esteganografía y hashes

Ocultar un mensaje dentro de una imagen, comprobar integridad con funciones hash, ver el efecto de la sal en contraseñas y relacionar los hashes con Git.

Herramientas: `steghide`, `md5sum`, `sha256sum`, `openssl`, `docker compose`, `git`.

### Esteganografía (ocultar) (`steghide`) 
```bash
# Ocultar el mensaje en la imagen (pide contraseña)
steghide embed -cf linus.jpg -ef mensaje -sf linus_steg.jpg
# -cf: imagen contenedora / -ef: mensaje / -sf: imagen de salida
# Extraer el mensaje oculto
steghide extract -sf linus_steg.jpg
```

Ejercicio Durruti: el mensaje está en una imagen de `durruti`, contraseña `durruti`, y el SHA-256 del archivo correcto es `7d573924d70a604cb56122aed9bded3f40d3083d8adc353a97c0b816c0e573bb`.

### Integridad (hashes) - DETERMINISTA

```bash
# md5sum: calcula el hash MD5 / sha256sum: calcula el hash SHA-256
md5sum integridad.txt
sha256sum integridad.txt

# Imagen original vs imagen con mensaje (no coinciden)
sha256sum linus.jpg
sha256sum linus_steg.jpg
```
### Contraseñas y sal

```bash
# Con sal: la misma contraseña da hashes distintos
openssl passwd -6 -salt SAL001 ContrasenaSegura
openssl passwd -6 -salt SAL002 ContrasenaSegura
# -6: Algoritmo SHA-512 crypt, -salt SAL001: fija la sal (SAL001)
```
# TODO: REVISAR ESTO
Demo web (`password_hash_demo`):

```bash
cd password_hash_demo
docker compose up --build
```

- `http://localhost:5001` — texto plano
- `http://localhost:5002` — hash SHA-256 (misma contraseña, mismo hash)
- `http://localhost:5003` — sal + PBKDF2-HMAC-SHA256 (misma contraseña, valor distinto por usuario)

### Hashes y Git

```bash
git clone git@github.com:mikel-egana-aranguren/EHU-SGSSI-01.git
cd EHU-SGSSI-01/
git log
```

El hash del commit identifica de forma única el árbol de archivos, los metadatos y el commit padre. Git compara hashes en lugar de comparar el contenido byte a byte.

---

## 2. Docker

Una imagen es la plantilla inmutable. Un contenedor es una ejecución de esa imagen.

```bash
sudo apt install docker.io
sudo groupadd docker
sudo usermod -aG docker $USER
# -aG: añade el usuario al grupo docker, sin quitarlo de los demás. Luego hay que reiniciar la sesión
```
### Imágenes
```bash
docker images
docker pull hello-world # baja desde servidor
docker rmi nombre_o_id # borrar imagen
```
### Contenedores
```bash 
docker run hello-world # creamos cont.
docker run -it ubuntu bash # crea imagen a partir de ubuntu y abre terminal bash (entrada y terminal abierta)
docker ps -a # listamos contenedores 
docker kill nombre_o_id # parar contenedor
docker rm nombre_o_id # borrar contenedor
docker exec nombre_container ls # ejecuta comando dentro de contenedor
```

### Construir una imagen

En el Dockerfile: `FROM` (imagen base), `ADD` (copiar archivos), `RUN` (comandos al construir), `CMD` (comando al arrancar).

```bash
docker build -t="nombre" . # teniendo el Dockerfile en el directorio
docker run nombre
```

```bash
docker run -it -v "$(pwd)"/dir-msg:/app ubuntu bash
# -v origen:destino. dir-msg/msg2 y /app/msg2 son espejos
cat /app/msg2
```

### Varios servicios (docker-lamp)

```bash
git clone https://github.com/mikel-egana-aranguren/docker-lamp.git
docker build -t="web" .
docker-compose up
docker-compose down
```
Tres servicios: la web en http://localhost:81, MariaDB y phpMyAdmin en http://localhost:8890 (usuario `admin`, contraseña `test`). Desde phpMyAdmin se importa `database.sql`. `down` para los servicios; `ctrl+c` también.

---

## 3. Cifrado simétrico

Tres programas, sin comandos de terminal:

- **César:** fuerza bruta del texto `Uunejvxb dw vdwmx wdnex jzdr, nw wdnbcaxb lxajixwnb` (detectar el castellano para dar con el desplazamiento).
- **Sustitución:** el texto está en castellano; se ataca por frecuencias de letras. Puede ser interactivo.
- **XOR:** cifrado de flujo byte a byte. Mensaje `ATAQUE AL AMANECER`, clave `CLAVE12345678901` (misma longitud). Cifrar y descifrar es la misma operación XOR.

### OpenSSL (`openssl enc`)

Cifrar con AES-256-CBC
```bash
openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -salt \
	-in mensaje.txt -out mensaje.aes -pass file:clave.txt

# -aes-256-cbc`: AES de 256 bits en modo CBC
# `-pbkdf2 -iter 100000`: deriva la clave a partir de la contraseña, repite el calculo 100000 veces
# `-pass file:clave.txt`: lee la contraseña del archivo
# -in mensaje.txt: el archivo de entrada
# -out mensaje.aes: archivo cifrado
# Ahora desciframos, `-d`: descifra
openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 \
	-in mensaje.aes -out mensaje.aes.descifrado -pass file:clave.txt
cmp mensaje.txt mensaje.aes.descifrado # compararlos

```
Triple DES y DES usan las mismas opciones. Cambian el algoritmo y hace falta el proveedor legacy (el actual no permite):

```bash
# Cifrar y descifrar en triple DES
openssl enc -des-ede3-cbc -provider default -provider legacy -pbkdf2 \
	-iter 100000 -salt -in mensaje.txt -out mensaje.3des -pass file:clave.txt
openssl enc -d -des-ede3-cbc -provider default -provider legacy -pbkdf2 \
	-iter 100000 -in mensaje.3des -out mensaje.3des.descifrado -pass file:clave.txt
cmp mensaje.txt mensaje.3des.descifrado

# Cifrar y descifrar en DES
openssl enc -des-cbc -provider default -provider legacy -pbkdf2 \
	-iter 100000 -salt -in mensaje.txt -out mensaje.des -pass file:clave.txt
openssl enc -d -des-cbc -provider default -provider legacy -pbkdf2 \
	-iter 100000 -in mensaje.des -out mensaje.des.descifrado -pass file:clave.txt
cmp mensaje.txt mensaje.des.descifrado

#Comprar los bashes SHA-256 de todos AES, DES, 3DES
sha256sum mensaje.txt mensaje.aes mensaje.3des mensaje.des
sha256sum mensaje.aes.descifrado mensaje.3des.descifrado mensaje.des.descifrado
```
Los tres cifrados tienen hash distinto entre sí y distinto del original. Los tres descifrados coinciden con `mensaje.txt`.

---

## 4. Cifrado asimétrico

La clave pública cifra y comprueba firmas. La privada descifra y firma.

### Comandos principales de GPG

```bash
gpg --generate-key                              # crea el par (pública y privada)
gpg --full-generate-key                         # igual, eligiendo algoritmo y longitud
gpg --list-keys                                 # lista las públicas. [ultimate] = confianza plena
gpg --list-secret-keys                          # lista las privadas
gpg --edit-key email                            # prompt de esa clave: trust, sign, save/quit
gpg --sign-key email 							# firmar la clave de alguien
gpg --delete-secret-keys email                  # borra la privada
gpg --delete-keys email                         # borra la pública
gpg --armor --export email > publica.asc        # exporta la pública en texto ASCII, sin armor lo muestra en binario
gpg --export-secret-keys --armor email > privada.asc
gpg --import archivo.asc                        # mete una clave en el llavero
# Firmar archivos
gpg --encrypt --recipient email archivo.txt     # confidencialidad: pública del destinatario
gpg --sign archivo.txt                          # integridad, autenticidad y no repudio: firmamos con la privada, sirve también para claves públicas pero poniendo el mail tal cual (no es firmar el archivo)
gpg --decrypt archivo.txt.gpg                   # descifra con tu privada
# Servidor: en ~/.gnupg/gpg.conf → keyserver hkps://keys.openpgp.org
gpg --send-keys KEY_ID                          # sube la pública. El id sale en --list-keys
gpg --search-keys email                         # busca en el servidor e importa
```


### 4 principios: firmar, cifrar, descifrar

```bash
gpg --encrypt --sign --recipient email archivo.txt          # confidencialidad, integridad, autenticidad y no repudio
gpg --decrypt archivo.txt.gpg  
```
Eso escribe como resultado el texto original ">" para escribir a un txt. 
### Confianza

En `--edit-key` del estudiante de confianza: `trust` → `5` (ultimate) → `quit`. Si esa persona ha firmado otra clave, la firmada pasa a `[full]`.

```bash
gpg --sign-key companero@email.com
gpg --export companero@email.com > companero_firmada.asc
```

El mismo esquema se puede hacer con el servidor: `--send-keys` para publicar, `--search-keys` para bajar la clave del compañero, firmarla y volver a subirla. 
IMPORTANTE: Esto no lo hemos probado pero se ve que opengpg por ataques bloqueó eso de poder subir la firma a la clave de otro. 

### Verificar un commit

```bash
gpg --verify archivo.asc archivo
git verify-commit 6176ac9c479797c698b153c7750fa3e4421f445d
```
La clave del profesor se importa con `--import` desde el `.asc`.

### Crear un commit firmado

```bash
git config --global user.signingkey KEY_ID
git config --global commit.gpgsign true
git commit -S -m "mensaje"
git log --show-signature
```

La clave que se pega en GitHub (Settings → SSH and GPG keys) es la de `--armor --export`. `-S` firma ese commit; con `commit.gpgsign true` los siguientes se firman solos.

TODO: REVISAR ESTO
### Revocar y cifrado simétrico

```bash
gpg --gen-revoke email > revoke_cert.asc
gpg --import revoke_cert.asc
gpg --send-keys KEY_ID
gpg --symmetric documento.md     est                         # una contraseña, sale .gpg
gpg --cipher-algo AES256 --armor --symmetric documento.md # sale .asc
gpg --decrypt documento.md.gpg > documento_descifrado.md
```

Una clave revocada no se puede recuperar. En simétrico emisor y receptor comparten la misma contraseña.

### RSA con OpenSSL

```bash
openssl genpkey -algorithm RSA -out clave.pem          # par completo
openssl rsa -text -in clave.pem                        # módulo, exponente y primos
openssl rsa -pubout -in clave.pem -out clave_publica.pem
openssl pkeyutl -encrypt -pubin -inkey clave_publica.pem -in mensaje.txt -out mensaje_cifrado.bin
openssl pkeyutl -decrypt -inkey clave.pem -in mensaje_cifrado.bin -out mensaje_descifrado.txt
```

`-pubin` indica que `-inkey` es una clave pública. RSA solo cifra bloques pequeños (unos 245 bytes con RSA-2048). Para un archivo grande, AES cifra el archivo y RSA cifra la clave AES.