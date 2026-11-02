# Laboratorio: NMap

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar lsi si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.
- Cuenta Google Cloud (ver laboratorio [Servidor remoto Google Cloud](../../Servidor_remoto_Google_Cloud/Servidor_remoto_Google_Cloud.md)).

## NMap

[Nmap](https://nmap.org/) es un programa de código abierto que sirve para rastrear puertos y máquinas en una red (probablemente sea la herramienta de hacking que aparece en más películas: [https://nmap.org/movies/](https://nmap.org/movies/)). Con Nmap se pueden descubrir fácilmente muchas características de las máquinas que están visibles en la red: qué máquinas están encendidas, qué puertos tiene abiertos una máquina concreta, qué servicios está ejecutando y qué versiones de los mismos, qué sistema operativo y qué versión usa, etc.

Instala NMap:

```bash
sudo apt install nmap
```

Describe los comandos necesarios para descubrir lo siguiente:

> ¿Qué puertos están abiertos en `scanme.nmap.org` y en tu servidor de Google Cloud, qué servicios y qué versión de esos servicios?

**Pasos:** Ejecuta la detección de servicios y versiones en el servidor de prueba de Nmap y en tu propia VM. Sustituye la IP por la IP pública de tu servidor:

```bash
nmap -sV scanme.nmap.org
nmap -sV -Pn 34.175.153.93
```

`-sV` intenta identificar el servicio y su versión; `-Pn` omite el descubrimiento inicial del host, que puede estar bloqueado por la red.

Resultado:
NMAP: Nmap scan report for scanme.nmap.org (45.33.32.156) ....

MI IP: Nmap scan report for 93.153.175.34.bc.googleusercontent.com (34.175.153.93)
Host is up.
All 1000 scanned ports on 93.153.175.34.bc.googleusercontent.com (34.175.153.93) are in ignored states.
......


> ¿Qué máquinas están activas en la red desde tu máquina hasta tu servidor remoto? (Pista: `traceroute`).


**Pasos:** Traza la ruta hasta tu VM. Cada salto corresponde a un router que responde; algunos no contestan y aparecen como `*`:

```bash
sudo apt install traceroute
traceroute -n 34.175.153.93
```


Instala `traceroute` si no está disponible (`sudo apt install traceroute`). Los saltos de la ruta no necesariamente son equipos que puedas explorar.

> ¿Qué puertos tiene abiertos una de las máquinas activas de la red?

**Pasos:** Elige una máquina propia o cuyo análisis esté autorizado y consulta sus puertos TCP más habituales. Yo he cogido el primer salto que es el router de casa supongo.

```bash
nmap -sT IP_AUTORIZADA
```

> ¿Qué versiones de los servicios está usando una de las máquinas activas de la red?

**Pasos:** Sobre esa misma máquina autorizada, solicita detección de versiones; opcionalmente limita el análisis a los puertos que aparecieron abiertos:

```bash
nmap -sV IP_AUTORIZADA
```
Por ejemplo un resultado:
22/tcp  open     ssh      Dropbear sshd 2019.78 (protocol 2.0)


> ¿Qué sistema operativo tiene una de las máquinas activas de la red?

**Pasos:** Prueba la detección de sistema operativo en una máquina autorizada. Suele requerir privilegios y la identificación es una estimación:

```bash
sudo nmap -O IP_AUTORIZADA
```

> ¿Qué sistema operativo tiene tu servidor en Google Cloud (según NMap)?

**Pasos:** Ejecuta la detección contra tu VM. Si el descubrimiento del host falla, usa `-Pn`:

```bash
sudo nmap -O -Pn IP_PUBLICA_DE_TU_VM
```


Aggressive OS guesses: HP P2000 G3 NAS device (89%), OpenWrt Kamikaze 7.09 (Linux 2.6.22) (86%),


> ¿Qué sistema operativo tiene `scanme.nmap.org`?

**Pasos:** El servidor está habilitado por Nmap para pruebas de escaneo. Solicita la detección de sistema operativo:

```bash
sudo nmap -O scanme.nmap.org
```
OS details: Linux 5.0 - 5.4

> Una vez determinado el sistema operativo, ¿qué vulnerabilidades tiene? (Pista: [https://cve.mitre.org](https://cve.mitre.org/)).


**Respuesta:** Nmap identificó `scanme.nmap.org` como Linux 5.0–5.4, pero es una estimación del sistema operativo y no indica la versión exacta del kernel ni sus parches. Por ello, ese resultado no permite afirmar qué CVE le afecta. En el router, Nmap identificó `Dropbear sshd 2019.78`; buscaría `Dropbear 2019.78` en MITRE CVE y en los avisos del fabricante, y comprobaría si las versiones afectadas incluyen esa versión. Solo se puede confirmar una vulnerabilidad con la versión exacta instalada y el estado de actualización; una coincidencia de producto o de familia de kernel es únicamente una pista para investigar.

> ¿Cómo se puede usar NMap para detectar si una máquina tiene un firewall?

**Pasos:** En un equipo propio o autorizado, consulta unos puertos conocidos y la razón que Nmap asigna a cada estado:

```bash
nmap -Pn -p 22,80,443 --reason IP_AUTORIZADA
```
PORT    STATE SERVICE REASON
22/tcp  open  ssh     syn-ack
80/tcp  open  http    syn-ack
443/tcp open  https   syn-ack

El estado `filtered` suele indicar que un filtro impide determinar si el puerto está abierto; `closed` significa que el host responde pero no hay un servicio escuchando. Esto no confirma por sí solo la presencia de un firewall: compara los resultados con las reglas configuradas y los registros del equipo.
