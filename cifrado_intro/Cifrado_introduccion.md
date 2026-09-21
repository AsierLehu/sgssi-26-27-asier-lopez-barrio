# Laboratorio: Introducción al cifrado, esteganografía y algoritmos resumen

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Herramientas necesarias: `openssl`, `sha512sum`, `git`, `steghide`, `docker`, `docker compose`.
- Repositorio GitHub de asignatura: puedes subir los programa desarrollados en el laboratorio.

## Esteganografía práctica

En este bloque ocultaremos un mensaje dentro de una imagen contenedora.

Si `steghide` no esta instalado:

```bash
sudo apt update
sudo apt install steghide -y
```

Preparar mensaje:

```bash
echo "SGSSI-26-27 Software is like sex: it's better when it's free" > msg_linus
```

Insertar mensaje con contraseña en imagen `linus.jpg`:

```bash
steghide embed -cf linus.jpg -ef msg_linus -sf linus_steg.jpg
```

**Explicación del comando embed:**
- `steghide embed`: comando para ocultar datos dentro de un archivo
- `-cf linus.jpg`: especifica el archivo contenedor (cover file) donde se ocultará el mensaje
- `-ef msg_linus`: especifica el archivo con el mensaje a ocultar (embed file)
- `-sf linus_steg.jpg`: especifica el nombre del archivo de salida (stego file) que contendrá la imagen con el mensaje oculto

Extracción del mensaje oculto (Primero renombrar archivo original mensaje a `msg_linus_old`):

```bash
steghide extract -sf linus_steg.jpg
less msg_linus
```

**Explicación de los comandos de extracción:**
- `steghide extract`: comando para extraer datos ocultos de un archivo
- `-sf linus_steg.jpg`: especifica el archivo que contiene los datos ocultos (stego file)
- `less msg_linus`: muestra el contenido del mensaje extraído usando el paginador less (permite navegar por el texto con las teclas de flecha)

Tamaño del contenedor:

```bash
ls -lh linus.jpg linus_steg.jpg
```

**Explicación del comando ls:**
- `ls -lh`: lista archivos en formato largo (-l) con tamaños legibles por humanos (-h)
- Compara los tamaños de la imagen original (`linus.jpg`) y la imagen con mensaje oculto (`linus_steg.jpg`) para verificar que el proceso de esteganografía no alteró significativamente el tamaño del archivo

## Integridad con funciones hash

Cálculo de resúmenes:

```bash
echo "Este fichero verifica integridad" > integridad.txt
md5sum integridad.txt
sha256sum integridad.txt
```

Modifica un solo caracter y vuelve a calcular los resúmenes. ¿Cómo han cambiado?

## Integridad y esteganografia

Compara los hashes de los mensajes usados en la esteganografía: 

```bash
sha256sum msg_linus
sha256sum msg_linus_old
```

¿Coinciden? 

Compara los hashes de los ficheros contenedor:

```bash
sha256sum linus.jpg
sha256sum linus_steg.jpg
```

¿Coinciden? 

Hay un mensaje importante de Buenaventura Durruti para vosotros en una de las imagenes del directorio `durruti`. El mensaje ha sido introducido mediante el programa steghide, con contraseña "durruti". La imagen que contiene el mensaje se corresponde con el Hash (SHA256) `7d573924d70a604cb56122aed9bded3f40d3083d8adc353a97c0b816c0e573bb`. ¿Qué archivo es? ¿Qué dice la frase? ¿Como automatizarías la búsqueda si tuvieses muchos archivos en carpetas y subcarpetas?

## Contraseñas y sal

Ejecuta:

```bash
echo -n "ContrasenaSegura" | sha256sum
echo -n "ContrasenaSegura" | sha256sum
```

Observa que el resultado es idéntico.

**Explicación:**
Este ejemplo demuestra una propiedad fundamental de las funciones hash criptográficas: son **deterministas**. Esto significa que el mismo input siempre produce exactamente el mismo output. En este caso:

- Ambos comandos calculan el hash SHA-256 de la cadena "ContrasenaSegura"


Uso de sal con OpenSSL:

```bash
openssl passwd -6 -salt SAL001 ContrasenaSegura
openssl passwd -6 -salt SAL002 ContrasenaSegura
```

**Explicación de los comandos:**

- `openssl passwd`: Comando de OpenSSL para generar hashes de contraseñas
- `-6`: Especifica el algoritmo SHA-512 crypt (método 6)
- `-salt SAL001` / `-salt SAL002`: Define la sal (salt) utilizada en cada caso
- `ContrasenaSegura`: La contraseña a procesar

**¿Qué hace la sal?**

La **sal** es una cadena aleatoria que se añade a la contraseña antes de calcular su hash. En este ejemplo:

1. **Primer comando**: Calcula el hash de "SAL001" + "ContrasenaSegura"
2. **Segundo comando**: Calcula el hash de "SAL002" + "ContrasenaSegura"

**Resultado esperado:**
Aunque la contraseña es idéntica ("ContrasenaSegura"), los hashes resultantes serán **completamente diferentes** debido a las distintas sales utilizadas.

¿Cambian los Hashes?

En la carpeta `password_hash_demo` tienes una pequeña aplicación web con tres versiones de la misma funcionalidad:

- `plain`: almacena la contraseña en texto plano.
- `hashed`: almacena un hash SHA-256 de la contraseña.
- `salted`: almacena unq sal aleatoria y un hash PBKDF2-HMAC-SHA256.

Para ejecutarla:

```bash
cd password_hash_demo
docker compose up --build
```

Después abre:

- http://localhost:5001/ -> versión insegura (texto plano)
- http://localhost:5002/ -> versión con hash
- http://localhost:5003/ -> versión con sal

Registra el mismo usuario y la misma contraseña en las tres versiones y compara la base de datos o la información mostrada por cada servicio. Fíjate en que:

- En texto plano se ve la contraseña original;
- Con hash, la misma contraseña produce el mismo valor hash para todos los usuarios;
- Con sal, cada usuario tiene una sal distinta, por lo que iguales contraseñas no generan el mismo valor almacenado.

Despliega el proyecto en tu servidor Google Cloud y comprueba que funciona correctamente, y que puedes cambiar la sal a un número definido por tí.

## Hashes y Git

Clona, si no lo has hecho ya, el repositorio de la asignatura (Usando SSH):

```bash
git clone git@github.com:mikel-egana-aranguren/EHU-SGSSI-01.git
cd cd EHU-SGSSI-01/
git log
```

¿Qué identifica el hash del commit?¿Por qué Git detecta cambios de contenido de forma eficiente?

**Respuesta:**

### ¿Qué identifica el hash del commit?

El hash SHA-1 (o SHA-256 en versiones más recientes) de un commit en Git identifica de forma **única e inequívoca** todo el estado del proyecto en ese momento específico. Este hash se calcula a partir de:

1. **El contenido completo del árbol de archivos** (tree object)
2. **Los metadatos del commit**: autor, fecha, mensaje, etc.
3. **El hash del commit padre** (commits anteriores)
4. **Cualquier cambio mínimo** en cualquiera de estos elementos

### ¿Por qué Git detecta cambios de contenido de forma eficiente?

Git utiliza las **propiedades criptográficas de las funciones hash** para optimizar la detección de cambios:

#### 1. **Comparación instantánea por hash**
- En lugar de comparar archivo por archivo, Git compara los hashes
- Si dos archivos tienen el mismo hash SHA-1, son **matemáticamente idénticos**
- Si los hashes difieren, los archivos son **definitivamente diferentes**

**En resumen**: Git convierte la costosa operación de "comparar contenido completo" en la rápida operación de "comparar números hash", manteniendo al mismo tiempo la garantía matemática de que la comparación es 100% precisa.


