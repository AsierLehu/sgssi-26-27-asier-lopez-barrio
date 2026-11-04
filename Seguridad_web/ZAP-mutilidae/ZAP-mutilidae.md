# Laboratorio: Pen-testing con ZAP y Mutillidae

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar usuario `lsi` si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.

## Pen-testing con ZAP y Mutillidae

El pen-testing consiste en buscar vulnerabilidades en sistemas Web. Para hacerlo vamos a usar un proyecto web vulnerable (Mutillidae) y un scaner de vulnerabilidades (ZAP).

## Desplegar Mutillidae 

Clona el repositorio de Mutillidae:

```bash
git clone https://github.com/webpwnized/mutillidae-dockerhub
```

Levanta el proyecto dentro de la carpeta `mutillidae-dockerhub`:

```bash
docker compose up
```
Ir a http://localhost:80. Si aparece un error del estilo "Database not set", pulsar en "Set up database".

## Instalar ZAP

Ir a https://www.zaproxy.org/download/, bajar el archivo `Linux package` y descomprimir. En el directorio apropiado, ejecutar ZAP:

```bash
./zap.sh
```

Elegir "Escaneo automático", http://localhost:80, y "atacar". Cuando termine el escaneo automático:

> ¿Qué vulnerabilidades has encontrado? ¿A qué CVEs o CWEs se mapean?

ZAP encontró cinco alertas: falta de las cabeceras CSP, Anti-Clickjacking y `X-Content-Type-Options`, filtrado de la versión del servidor y divulgación de información en el banner. Se relacionan principalmente con **CWE-693**, **CWE-1021**, **CWE-497**, **CWE-200** y **WASC-13/15**. No tienen un CVE concreto porque son problemas de configuración o de divulgación de
información. Por ejemplo, la alerta CSP de la captura indica `CWE-693` y `WASC-15`.

> Intenta realizar el escaneo en la IP Google Cloud proporcionada por el profesor, ¿Has encontrado las mismas vulnerabilidades?

Deberían aparecer vulnerabilidades similares, especialmente las relacionadas con las cabeceras HTTP y la divulgación de información. El resultado puede variar según la configuración del servidor, la versión de Mutillidae y las reglas activas en ZAP.
